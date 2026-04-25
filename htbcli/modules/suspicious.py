"""
Suspicious activity analysis module for HTB CLI
"""

import click
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

# Thresholds
CRITICAL_USER_ROOT_SECS = 30
HIGH_USER_ROOT_SECS = 120
BURST_WINDOW_MINUTES = 60
BURST_MIN_MACHINES = 4
DORMANCY_DAYS = 30


class SuspiciousModule:
    """Module for analyzing suspicious activity patterns on HTB user profiles"""

    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
        self._machine_cache: Dict[str, Dict] = {}

    def get_profile(self, user_id: int) -> Dict[str, Any]:
        return self.api.get(f"/user/profile/basic/{user_id}")

    def get_activity(self, user_id: int) -> Dict[str, Any]:
        return self.api.get(f"/user/profile/activity/{user_id}")

    def get_bloods(self, user_id: int) -> Dict[str, Any]:
        return self.api.get(f"/user/profile/bloods/{user_id}")

    def get_machine_release(self, machine_name: str) -> Optional[str]:
        """Return release datetime for a machine, cached to avoid repeat calls."""
        key = machine_name.lower()
        if key not in self._machine_cache:
            try:
                info = self.api.get(f"/machine/profile/{key}").get("info", {})
                self._machine_cache[key] = info.get("release")
            except Exception:
                self._machine_cache[key] = None
        return self._machine_cache[key]

    def search_user_by_name(self, username: str) -> Optional[int]:
        """Search for a user by username and return their ID."""
        from .platform import PlatformModule
        result = PlatformModule(self.api).get_search_fetch(username)
        if not result or not result.get("users"):
            return None
        search_term = username.lower()
        exact, partial = [], []
        for u in result["users"]:
            name = u.get("value", "").lower()
            uid = u.get("id")
            if name == search_term:
                exact.append(uid)
            elif search_term in name:
                partial.append(uid)
        if exact:
            return exact[0]
        if partial:
            return partial[0]
        return None

    def resolve_user(self, identifier: str) -> Optional[int]:
        """Resolve a username or numeric string to a user ID."""
        if identifier.isdigit():
            return int(identifier)
        uid = self.search_user_by_name(identifier)
        if uid is None:
            console.print(f"[red]Could not find user: {identifier}[/red]")
        return uid

    def analyze(self, user_id: int, enrich_release: bool = False) -> Dict[str, Any]:
        activity_data = self.get_activity(user_id)
        activities = activity_data.get("profile", {}).get("activity", [])

        burst_sessions = _check_bursts(activities)

        for b in burst_sessions:
            b["details"] = _burst_machine_details(activities, b)

        if enrich_release:
            for b in burst_sessions:
                if b.get("object_type") == "machine":
                    for md in b["details"]:
                        md["release"] = self.get_machine_release(md["name"])

        findings = {
            "burst_sessions": burst_sessions,
            "dormancy_bursts": _check_dormancy_bursts(activities),
            "fast_challenges": _check_fast_challenges(activities),
            "fast_fortresses": _check_fast_fortresses(activities),
        }

        findings["score"] = _compute_score(findings)
        findings["total_activities"] = len(activities)
        findings["machines_completed"] = _count_completed_machines(activities)
        findings["activity_span_days"] = _activity_span(activities)
        return findings


# ── Analysis helpers ──────────────────────────────────────────────────────────

def _parse_dt(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))


def _check_fast_completions(activities: List[Dict]) -> List[Dict]:
    """Find machines where user→root delta is very short (informational; low weight on retired boxes)."""
    machine_events: Dict[int, Dict[str, datetime]] = defaultdict(dict)
    for a in activities:
        if a.get("object_type") != "machine":
            continue
        mid = a["id"]
        t = _parse_dt(a["date"])
        if a["type"] == "user":
            machine_events[mid]["user"] = t
            machine_events[mid]["name"] = a["name"]
        elif a["type"] == "root":
            machine_events[mid]["root"] = t
            machine_events[mid]["name"] = a["name"]
            machine_events[mid]["points"] = a.get("points", 0)

    results = []
    for mid, ev in machine_events.items():
        if "user" not in ev or "root" not in ev:
            continue
        delta = abs((ev["root"] - ev["user"]).total_seconds())
        if delta < HIGH_USER_ROOT_SECS:
            severity = "CRITICAL" if delta < CRITICAL_USER_ROOT_SECS else "HIGH"
            results.append({
                "machine_id": mid,
                "name": ev["name"],
                "user_time": ev["user"].isoformat(),
                "root_time": ev["root"].isoformat(),
                "delta_seconds": int(delta),
                "severity": severity,
                "points": ev.get("points", 0),
            })
    return sorted(results, key=lambda x: x["delta_seconds"])


def _check_impossible_speed(activities: List[Dict]) -> List[Dict]:
    """Subset of fast completions below the physical minimum (~10s)."""
    fast = _check_fast_completions(activities)
    return [f for f in fast if f["delta_seconds"] < 15]



def _check_bursts_for(
    activities: List[Dict],
    object_type: str,
    flag_type: Optional[str],
    window_minutes: int,
    min_count: int,
) -> List[Dict]:
    """Generic burst detector for any activity type."""
    events = sorted(
        [
            a for a in activities
            if a.get("object_type") == object_type
            and (flag_type is None or a.get("type") == flag_type)
        ],
        key=lambda x: x["date"],
    )
    bursts = []
    i = 0
    while i < len(events):
        window_start = _parse_dt(events[i]["date"])
        window_end = window_start + timedelta(minutes=window_minutes)
        cluster = [events[i]]
        j = i + 1
        while j < len(events) and _parse_dt(events[j]["date"]) <= window_end:
            cluster.append(events[j])
            j += 1
        if len(cluster) >= min_count:
            bursts.append({
                "object_type": object_type,
                "start": events[i]["date"],
                "end": cluster[-1]["date"],
                "count": len(cluster),
                "names": [e["name"] for e in cluster],
                "duration_minutes": int(
                    (_parse_dt(cluster[-1]["date"]) - window_start).total_seconds() / 60
                ),
            })
            i = j
        else:
            i += 1
    return bursts


def _check_bursts(activities: List[Dict]) -> List[Dict]:
    """Burst detection across machines, challenges, and fortresses."""
    return (
        _check_bursts_for(activities, "machine",   "root",      BURST_WINDOW_MINUTES, BURST_MIN_MACHINES)
        + _check_bursts_for(activities, "challenge", "challenge", 30,                  3)
        + _check_bursts_for(activities, "fortress",  "fortress",  30,                  3)
    )


def _check_dormancy_bursts(activities: List[Dict]) -> List[Dict]:
    """Detect long inactivity periods followed by sudden activity spikes."""
    root_events = sorted(
        [a for a in activities if a.get("object_type") == "machine" and a["type"] == "root"],
        key=lambda x: x["date"],
    )
    if len(root_events) < 2:
        return []
    results = []
    for i in range(1, len(root_events)):
        prev_dt = _parse_dt(root_events[i - 1]["date"])
        curr_dt = _parse_dt(root_events[i]["date"])
        gap_days = (curr_dt - prev_dt).days
        if gap_days >= DORMANCY_DAYS:
            # Count burst after resumption (machines in next 7 days)
            week_end = curr_dt + timedelta(days=7)
            burst_count = sum(
                1 for e in root_events[i:]
                if _parse_dt(e["date"]) <= week_end
            )
            results.append({
                "gap_end": root_events[i]["date"],
                "gap_days": gap_days,
                "machines_after_gap_7d": burst_count,
                "first_machine_after": root_events[i]["name"],
            })
    return results


def _check_fast_consecutive(activities: List[Dict], object_type: str, window_secs: int = 120) -> List[Dict]:
    """
    Check for suspiciously fast consecutive flag submissions.
    - Challenges: each is an independent CTF-style flag, quick succession = likely automation.
    - Fortresses: flags are NOT independent puzzles; they are known to leak. Quick fortress
      submissions strongly suggest a user has a pre-compiled list of leaked flags.
    """
    events = sorted(
        [a for a in activities if a.get("object_type") == object_type],
        key=lambda x: x["date"],
    )
    results = []
    for i in range(1, len(events)):
        prev = events[i - 1]
        curr = events[i]
        delta = int(abs((_parse_dt(curr["date"]) - _parse_dt(prev["date"])).total_seconds()))
        if delta < window_secs:
            severity = "CRITICAL" if delta < 20 else "HIGH"
            results.append({
                "from": prev["name"],
                "to": curr["name"],
                "delta_seconds": delta,
                "severity": severity,
                "time": curr["date"],
                "category": curr.get("challenge_category") or curr.get("type", "?"),
                "object_type": object_type,
            })
    return sorted(results, key=lambda x: x["delta_seconds"])


def _check_fast_challenges(activities: List[Dict]) -> List[Dict]:
    return _check_fast_consecutive(activities, "challenge")


def _check_fast_fortresses(activities: List[Dict]) -> List[Dict]:
    return _check_fast_consecutive(activities, "fortress")


def _burst_machine_details(activities: List[Dict], burst: Dict) -> List[Dict]:
    """Return per-flag submission rows for each machine inside a burst window."""
    start_dt = _parse_dt(burst["start"])
    end_dt = _parse_dt(burst["end"])
    otype = burst.get("object_type", "machine")
    rows = []
    for a in activities:
        if a.get("object_type") != otype:
            continue
        dt = _parse_dt(a["date"])
        if start_dt <= dt <= end_dt:
            rows.append({
                "name": a["name"],
                "flag": a["type"],
                "date": a["date"],
                "points": a.get("points", 0),
                "category": a.get("challenge_category", ""),
            })
    return sorted(rows, key=lambda x: x["date"])



def _count_completed_machines(activities: List[Dict]) -> int:
    seen = set()
    for a in activities:
        if a.get("object_type") == "machine" and a["type"] == "root":
            seen.add(a["id"])
    return len(seen)


def _activity_span(activities: List[Dict]) -> int:
    if not activities:
        return 0
    dates = [_parse_dt(a["date"]) for a in activities]
    return (max(dates) - min(dates)).days


def _difficulty_weight(points: int) -> float:
    """Convert HTB points to a difficulty multiplier (easy=1x, insane=3x)."""
    if points >= 50:
        return 3.0
    if points >= 30:
        return 2.0
    if points >= 20:
        return 1.5
    if points >= 10:
        return 1.2
    return 1.0  # 0-pt starting-point machines


def _compute_score(findings: Dict) -> int:
    """
    Heuristic suspicion score 0-100.

    Signals (strongest to weakest):
    - Fortress bursts: leaked flags, physically impossible to solve that fast
    - Challenge bursts: independent flags submitted in rapid succession
    - Machine bursts: many boxes rooted in a short window
    - Fast fortress consecutive: direct leaked-flag indicator
    - Fast challenge consecutive: automation indicator
    - Dormancy → burst: contextual, mild weight

    NOT scored: user→root delta — on retired boxes people batch-submit both
    flags at the end of a writeup run, making this a false-positive factory.
    """
    score = 0.0

    burst_weights = {"machine": 6, "challenge": 10, "fortress": 15}
    for b in findings["burst_sessions"]:
        w = burst_weights.get(b.get("object_type", "machine"), 6)
        score += b["count"] * w

    for f in findings.get("fast_challenges", []):
        score += 25 if f["severity"] == "CRITICAL" else 12

    for f in findings.get("fast_fortresses", []):
        score += 35 if f["severity"] == "CRITICAL" else 20

    score += len(findings["dormancy_bursts"]) * 2

    return min(int(score), 100)


def _severity_color(severity: str) -> str:
    return {"CRITICAL": "red", "HIGH": "yellow", "MEDIUM": "orange3", "LOW": "green"}.get(severity, "white")


def _score_label(score: int) -> Tuple[str, str]:
    if score >= 60:
        return "HIGH", "red"
    if score >= 30:
        return "MEDIUM", "yellow"
    if score >= 10:
        return "LOW", "green"
    return "CLEAN", "bright_green"


# ── Click commands ────────────────────────────────────────────────────────────

@click.group()
def suspicious():
    """Analyze HTB user profiles for suspicious activity patterns"""
    pass


@suspicious.command()
@click.argument("user", type=str)
@click.option("--debug", is_flag=True, help="Show raw API response")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--release-dates", is_flag=True, help="Fetch machine release dates (makes extra API calls, slow on large profiles)")
def analyze(user: str, debug: bool, json_output: bool, release_dates: bool):
    """Full suspicious activity analysis for a user (username or ID)"""
    try:
        api = HTBAPIClient()
        mod = SuspiciousModule(api)
        user_id = mod.resolve_user(user)
        if user_id is None:
            return

        profile_data = mod.get_profile(user_id)
        if handle_debug_option(debug, profile_data, "Debug: Profile", json_output):
            return

        profile = profile_data.get("profile", {})
        username = profile.get("name", str(user_id))

        findings = mod.analyze(user_id, enrich_release=release_dates)
        score = findings["score"]
        label, label_color = _score_label(score)

        console.print(Panel.fit(
            f"[bold]User:[/bold] [cyan]{username}[/cyan]  (ID: {user_id})\n"
            f"[bold]Activities:[/bold] {findings['total_activities']}  "
            f"[bold]Machines:[/bold] {findings['machines_completed']}  "
            f"[bold]Span:[/bold] {findings['activity_span_days']} days\n"
            f"[bold]Suspicion Score:[/bold] [{label_color}]{score}/100 — {label}[/{label_color}]",
            title="[bold red]Suspicious Activity Report[/bold red]",
            border_style="red" if score >= 60 else "yellow" if score >= 30 else "green",
        ))

        # Burst sessions — per-type detail
        if findings["burst_sessions"]:
            for bi, b in enumerate(findings["burst_sessions"], 1):
                otype = b.get("object_type", "machine")
                is_machine = otype == "machine"
                t3 = Table(
                    title=f"Burst #{bi} \\[{otype}] — {b['count']} items in {b['duration_minutes']}m",
                    box=box.SIMPLE_HEAVY,
                )
                t3.add_column("Name", style="cyan")
                if is_machine:
                    t3.add_column("Released", style="dim")
                else:
                    t3.add_column("Category", style="dim")
                t3.add_column("Flag")
                t3.add_column("Submitted At")
                t3.add_column("Pts", justify="right")
                prev_dt = None
                for md in b.get("details", []):
                    dt = _parse_dt(md["date"])
                    delta_str = ""
                    if prev_dt is not None:
                        secs = int((dt - prev_dt).total_seconds())
                        delta_str = f" (+{secs}s)"
                    flag_style = "green" if md["flag"] == "user" else "red"
                    col2 = (md.get("release") or "")[:10] or "?" if is_machine else (md.get("category") or "")
                    t3.add_row(
                        md["name"],
                        col2,
                        f"[{flag_style}]{md['flag']}[/{flag_style}]",
                        md["date"][:19] + delta_str,
                        str(md["points"]),
                    )
                    prev_dt = dt
                console.print(t3)

        # Dormancy bursts
        if findings["dormancy_bursts"]:
            t4 = Table(title="Dormancy → Burst Patterns", box=box.SIMPLE_HEAVY)
            t4.add_column("Gap End", style="magenta")
            t4.add_column("Gap (days)", justify="right")
            t4.add_column("Machines (next 7d)", justify="right")
            t4.add_column("First Machine After")
            for d in findings["dormancy_bursts"]:
                t4.add_row(
                    d["gap_end"][:10],
                    str(d["gap_days"]),
                    str(d["machines_after_gap_7d"]),
                    d["first_machine_after"],
                )
            console.print(t4)

        # Fast challenge completions
        if findings.get("fast_challenges"):
            t5 = Table(title="Fast Consecutive Challenge Completions", box=box.SIMPLE_HEAVY)
            t5.add_column("From", style="cyan")
            t5.add_column("To", style="cyan")
            t5.add_column("Delta (s)", justify="right")
            t5.add_column("Severity")
            t5.add_column("Category")
            for f in findings["fast_challenges"]:
                color = _severity_color(f["severity"])
                t5.add_row(
                    f["from"],
                    f["to"],
                    str(f["delta_seconds"]),
                    f"[{color}]{f['severity']}[/{color}]",
                    f["category"],
                )
            console.print(t5)

        # Fast fortress submissions (leaked flag indicator)
        if findings.get("fast_fortresses"):
            t6 = Table(title="[red]Fast Fortress Submissions (leaked flag indicator)[/red]", box=box.SIMPLE_HEAVY)
            t6.add_column("From", style="cyan")
            t6.add_column("To", style="cyan")
            t6.add_column("Delta (s)", justify="right")
            t6.add_column("Severity")
            for f in findings["fast_fortresses"]:
                color = _severity_color(f["severity"])
                t6.add_row(
                    f["from"],
                    f["to"],
                    str(f["delta_seconds"]),
                    f"[{color}]{f['severity']}[/{color}]",
                )
            console.print(t6)


        if score == 0:
            console.print("[green]No suspicious patterns detected.[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@suspicious.command()
@click.argument("user", type=str)
@click.option("--debug", is_flag=True, help="Show raw API response")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def speed(user: str, debug: bool, json_output: bool):
    """Show only fast user→root completion times for a user (username or ID)"""
    try:
        api = HTBAPIClient()
        mod = SuspiciousModule(api)
        user_id = mod.resolve_user(user)
        if user_id is None:
            return
        data = mod.get_activity(user_id)

        if handle_debug_option(debug, data, "Debug: Activity", json_output):
            return

        activities = data.get("profile", {}).get("activity", [])
        fast = _check_fast_completions(activities)

        if not fast:
            console.print("[green]No suspiciously fast completions found.[/green]")
            return

        t = Table(title=f"Fast Completions — User {user_id}", box=box.SIMPLE_HEAVY)
        t.add_column("Machine", style="cyan")
        t.add_column("Delta (s)", justify="right")
        t.add_column("Severity")
        for f in fast:
            color = _severity_color(f["severity"])
            t.add_row(f["name"], str(f["delta_seconds"]), f"[{color}]{f['severity']}[/{color}]")
        console.print(t)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@suspicious.command()
@click.argument("user", type=str)
@click.option("--debug", is_flag=True, help="Show raw API response")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def bursts(user: str, debug: bool, json_output: bool):
    """Show burst sessions (many machines in short time window) (username or ID)"""
    try:
        api = HTBAPIClient()
        mod = SuspiciousModule(api)
        user_id = mod.resolve_user(user)
        if user_id is None:
            return
        data = mod.get_activity(user_id)

        if handle_debug_option(debug, data, "Debug: Activity", json_output):
            return

        activities = data.get("profile", {}).get("activity", [])
        burst_list = _check_bursts(activities)

        if not burst_list:
            console.print("[green]No burst sessions detected.[/green]")
            return

        t = Table(title=f"Burst Sessions — User {user_id}", box=box.SIMPLE_HEAVY)
        t.add_column("Type", style="magenta")
        t.add_column("Start", style="yellow")
        t.add_column("Count", justify="right")
        t.add_column("Duration")
        t.add_column("Names")
        for b in burst_list:
            t.add_row(b.get("object_type","?"), b["start"][:19], str(b["count"]), f"{b['duration_minutes']}m", ", ".join(b["names"]))
        console.print(t)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@suspicious.command()
@click.argument("user", type=str)
@click.option("--debug", is_flag=True, help="Show raw API response")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def score(user: str, debug: bool, json_output: bool):
    """Print a single suspicion score (0-100) for a user (username or ID)"""
    try:
        api = HTBAPIClient()
        mod = SuspiciousModule(api)
        user_id = mod.resolve_user(user)
        if user_id is None:
            return
        findings = mod.analyze(user_id)

        if handle_debug_option(debug, findings, "Debug: Findings", json_output):
            return

        s = findings["score"]
        label, color = _score_label(s)
        console.print(f"User [cyan]{user_id}[/cyan] suspicion score: [{color}]{s}/100 ({label})[/{color}]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@suspicious.command(name="challenges")
@click.argument("user", type=str)
@click.option("--debug", is_flag=True, help="Show raw API response")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def challenges_speed(user: str, debug: bool, json_output: bool):
    """Show suspiciously fast consecutive challenge completions (username or ID)"""
    try:
        api = HTBAPIClient()
        mod = SuspiciousModule(api)
        user_id = mod.resolve_user(user)
        if user_id is None:
            return
        data = mod.get_activity(user_id)

        if handle_debug_option(debug, data, "Debug: Activity", json_output):
            return

        activities = data.get("profile", {}).get("activity", [])
        fast = _check_fast_challenges(activities)

        if not fast:
            console.print("[green]No suspiciously fast challenge completions found.[/green]")
            return

        t = Table(title=f"Fast Challenge Completions — User {user_id}", box=box.SIMPLE_HEAVY)
        t.add_column("From Challenge", style="cyan")
        t.add_column("To Challenge", style="cyan")
        t.add_column("Delta (s)", justify="right")
        t.add_column("Severity")
        t.add_column("Category")
        for f in fast:
            color = _severity_color(f["severity"])
            t.add_row(
                f["from"],
                f["to"],
                str(f["delta_seconds"]),
                f"[{color}]{f['severity']}[/{color}]",
                f["category"],
            )
        console.print(t)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
