"""
Academy x Labs relations module for HTB CLI.

Wraps the public, unauthenticated endpoints behind
https://academy.hackthebox.com/academy-lab-relations:

  GET /api/v2/external/public/labs/{category}                  -> list items
  GET /api/v2/external/public/labs/relations/{category}/{id}   -> related items

Categories: modules, machines, exams, fortresses, prolabs, sherlocks.
"""

import click
import requests
from typing import Any, Dict, List, Optional, Tuple
from rich.console import Console
from rich.table import Table

console = Console()

BASE = "https://academy.hackthebox.com/api/v2/external/public/labs"
CATEGORIES = ("modules", "machines", "exams", "fortresses", "prolabs", "sherlocks")
CATEGORY_ALIASES = {
    "module": "modules", "modules": "modules",
    "machine": "machines", "machines": "machines", "box": "machines", "boxes": "machines",
    "exam": "exams", "exams": "exams",
    "fortress": "fortresses", "fortresses": "fortresses",
    "prolab": "prolabs", "prolabs": "prolabs",
    "sherlock": "sherlocks", "sherlocks": "sherlocks",
}


def _get(path: str) -> Dict[str, Any]:
    r = requests.get(f"{BASE}{path}", headers={"Accept": "application/json"}, timeout=20)
    r.raise_for_status()
    return r.json()


def _list_category(category: str) -> List[Dict[str, Any]]:
    return _get(f"/{category}").get("data", [])


def _get_relations(category: str, item_id: int) -> Dict[str, List[Dict[str, Any]]]:
    return _get(f"/relations/{category}/{item_id}").get("data", {})


def _resolve(category: str, identifier: str) -> Optional[Tuple[int, str]]:
    """Resolve an identifier (numeric ID, slug, or name) to (id, display_name)."""
    items = _list_category(category)
    try:
        wanted = int(identifier)
        for it in items:
            if it.get("id") == wanted:
                return wanted, it.get("name", str(wanted))
    except ValueError:
        pass

    needle = identifier.strip().lower()
    for it in items:
        if str(it.get("slug", "")).lower() == needle:
            return it["id"], it.get("name", needle)
    for it in items:
        if str(it.get("name", "")).lower() == needle:
            return it["id"], it["name"]
    matches = [it for it in items if needle in str(it.get("name", "")).lower()
               or needle in str(it.get("slug", "")).lower()]
    if len(matches) == 1:
        return matches[0]["id"], matches[0].get("name", needle)
    if len(matches) > 1:
        names = ", ".join(f"{m.get('name')} (id={m.get('id')})" for m in matches[:8])
        console.print(f"[yellow]Ambiguous {category} match for '{identifier}': {names}{' ...' if len(matches) > 8 else ''}[/yellow]")
    return None


def _print_items_table(category: str, items: List[Dict[str, Any]]) -> None:
    table = Table(title=f"Academy/Labs: {category} ({len(items)})")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="green")
    if category == "modules":
        table.add_column("Slug", style="magenta")
        table.add_column("Difficulty", style="yellow")
        table.add_column("Tier", style="blue")
    elif category == "machines":
        table.add_column("OS", style="magenta")
        table.add_column("Difficulty", style="yellow")
    elif category == "exams":
        table.add_column("Slug", style="magenta")
    elif category == "fortresses":
        table.add_column("Flags", style="yellow", justify="right")
    elif category == "prolabs":
        table.add_column("Difficulty", style="yellow")
    elif category == "sherlocks":
        table.add_column("Category", style="magenta")
        table.add_column("Difficulty", style="yellow")
    table.add_column("Relations", style="white")

    for it in items:
        rel = it.get("aggregates", {}).get("relations", {}) or {}
        rel_str = " ".join(f"{k.replace('total_', '')[:3]}={v}" for k, v in rel.items() if v)
        row = [str(it.get("id", "")), str(it.get("name", ""))]
        if category == "modules":
            diff = (it.get("difficulty") or {}).get("text", "")
            tier = (it.get("tier") or {}).get("name", "")
            row += [str(it.get("slug", "")), diff, tier]
        elif category == "machines":
            row += [str(it.get("os", "")), str(it.get("difficulty", ""))]
        elif category == "exams":
            row += [str(it.get("slug", ""))]
        elif category == "fortresses":
            row += [str(it.get("number_of_flags", ""))]
        elif category == "prolabs":
            row += [str(it.get("difficulty", ""))]
        elif category == "sherlocks":
            row += [str(it.get("category", "")), str(it.get("difficulty", ""))]
        row.append(rel_str or "-")
        table.add_row(*row)
    console.print(table)


def _print_relations(category: str, item_id: int, item_name: str,
                     rels: Dict[str, List[Dict[str, Any]]]) -> None:
    total = sum(len(v) for v in rels.values())
    console.print(f"\n[bold]{category[:-1].capitalize()} '{item_name}' (id={item_id})[/bold] -> {total} related item(s)\n")
    if not total:
        console.print("[yellow]No relations.[/yellow]")
        return

    for rel_cat, items in rels.items():
        if not items:
            continue
        table = Table(title=f"{rel_cat} ({len(items)})")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name", style="green")
        if rel_cat == "modules":
            table.add_column("Slug", style="magenta")
            table.add_column("Difficulty", style="yellow")
        elif rel_cat == "machines":
            table.add_column("OS", style="magenta")
            table.add_column("Difficulty", style="yellow")
        elif rel_cat == "exams":
            table.add_column("Slug", style="magenta")
        elif rel_cat == "sherlocks":
            table.add_column("Category", style="magenta")
            table.add_column("Difficulty", style="yellow")
        elif rel_cat == "prolabs":
            table.add_column("Difficulty", style="yellow")

        for it in items:
            row = [str(it.get("id", "")), str(it.get("name", ""))]
            if rel_cat == "modules":
                diff = it.get("difficulty")
                if isinstance(diff, dict):
                    diff = diff.get("text", "")
                row += [str(it.get("slug", "")), str(diff or "")]
            elif rel_cat == "machines":
                row += [str(it.get("os", "")), str(it.get("difficulty", ""))]
            elif rel_cat == "exams":
                row += [str(it.get("slug", ""))]
            elif rel_cat == "sherlocks":
                row += [str(it.get("category", "")), str(it.get("difficulty", ""))]
            elif rel_cat == "prolabs":
                row += [str(it.get("difficulty", ""))]
            table.add_row(*row)
        console.print(table)


def _lookup_and_print(category: str, identifier: str) -> None:
    resolved = _resolve(category, identifier)
    if not resolved:
        console.print(f"[red]No {category[:-1]} found matching '{identifier}'.[/red] "
                      f"Try: htbcli academyxlabs list {category}")
        return
    item_id, name = resolved
    rels = _get_relations(category, item_id)
    _print_relations(category, item_id, name, rels)


@click.group(invoke_without_command=True)
@click.option("-m", "--module", "module_id", help="Module name/slug/ID — show related items.")
@click.option("-M", "--machine", "machine_id", help="Machine name/ID — show related items.")
@click.option("-e", "--exam", "exam_id", help="Exam name/slug/ID — show related items.")
@click.option("-f", "--fortress", "fortress_id", help="Fortress name/ID — show related items.")
@click.option("-p", "--prolab", "prolab_id", help="Prolab name/ID — show related items.")
@click.option("-s", "--sherlock", "sherlock_id", help="Sherlock name/ID — show related items.")
@click.pass_context
def academyxlabs(ctx, module_id, machine_id, exam_id, fortress_id, prolab_id, sherlock_id):
    """Academy <-> Labs relations (modules, machines, exams, fortresses, prolabs, sherlocks)."""
    pairs = [
        ("modules", module_id),
        ("machines", machine_id),
        ("exams", exam_id),
        ("fortresses", fortress_id),
        ("prolabs", prolab_id),
        ("sherlocks", sherlock_id),
    ]
    selected = [(c, v) for c, v in pairs if v]
    if selected:
        if ctx.invoked_subcommand:
            console.print("[yellow]Ignoring subcommand because a category flag was given.[/yellow]")
        for category, ident in selected:
            try:
                _lookup_and_print(category, ident)
            except requests.HTTPError as e:
                console.print(f"[red]HTTP error for {category} '{ident}': {e}[/red]")
            except Exception as e:
                console.print(f"[red]Error for {category} '{ident}': {e}[/red]")
        return

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@academyxlabs.command("categories")
def cmd_categories():
    """List the available categories."""
    table = Table(title="Categories")
    table.add_column("Category", style="cyan")
    table.add_column("Flag", style="green")
    flag_map = {"modules": "-m", "machines": "-M", "exams": "-e",
                "fortresses": "-f", "prolabs": "-p", "sherlocks": "-s"}
    for c in CATEGORIES:
        table.add_row(c, flag_map[c])
    console.print(table)


@academyxlabs.command("list")
@click.argument("category")
def cmd_list(category):
    """List items in a category (modules, machines, exams, fortresses, prolabs, sherlocks)."""
    cat = CATEGORY_ALIASES.get(category.lower())
    if not cat:
        console.print(f"[red]Unknown category '{category}'.[/red] Valid: {', '.join(CATEGORIES)}")
        return
    try:
        items = _list_category(cat)
    except Exception as e:
        console.print(f"[red]Error fetching {cat}: {e}[/red]")
        return
    _print_items_table(cat, items)


@academyxlabs.command("relations")
@click.argument("category")
@click.argument("identifier")
def cmd_relations(category, identifier):
    """Show relations for an item: CATEGORY IDENTIFIER (name, slug, or ID)."""
    cat = CATEGORY_ALIASES.get(category.lower())
    if not cat:
        console.print(f"[red]Unknown category '{category}'.[/red] Valid: {', '.join(CATEGORIES)}")
        return
    try:
        _lookup_and_print(cat, identifier)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# Backwards-compat-ish alias for the module class pattern used by other modules
class AcademyXLabsModule:
    """Thin wrapper exposing the same calls programmatically."""
    @staticmethod
    def list(category: str) -> List[Dict[str, Any]]:
        return _list_category(CATEGORY_ALIASES.get(category.lower(), category))

    @staticmethod
    def relations(category: str, identifier) -> Dict[str, List[Dict[str, Any]]]:
        cat = CATEGORY_ALIASES.get(str(category).lower(), category)
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            return _get_relations(cat, int(identifier))
        resolved = _resolve(cat, str(identifier))
        if not resolved:
            return {}
        return _get_relations(cat, resolved[0])
