"""
VPN module for HTB CLI
"""

import os
import subprocess
import click
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path

from ..api_client import HTBAPIClient

console = Console()

class VPNModule:
    """Module for handling VPN-related operations"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
        self.vpn_dir = Path.home() / ".htbcli" / "vpn"
        self.vpn_dir.mkdir(parents=True, exist_ok=True)
    
    def get_vpn_servers(self, product: str = "labs") -> Dict[str, Any]:
        """Get list of VPN servers"""
        return self.api.get("/connections/servers", params={"product": product})
    
    def download_vpn_config(self, vpn_id: int, protocol: str = "udp") -> bytes:
        """Download VPN configuration file"""
        if protocol.lower() == "tcp":
            return self.api.get_binary(f"/access/ovpnfile/{vpn_id}/0/1")
        else:
            return self.api.get_binary(f"/access/ovpnfile/{vpn_id}/0")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current VPN connection status"""
        return self.api.get("/connection/status")
    
    def switch_vpn_server(self, vpn_id: int) -> Dict[str, Any]:
        """Switch VPN server"""
        return self.api.post(f"/connections/servers/switch/{vpn_id}", json_data={})
    
    def download_all_vpns(self) -> List[Dict[str, Any]]:
        """Download all available VPN configurations"""
        servers = self.get_vpn_servers()
        downloaded = []
        
        if servers and isinstance(servers, dict) and 'data' in servers:
            data = servers['data']
            
            # Parse the nested structure
            if 'options' in data:
                for location, location_data in data['options'].items():
                    for server_type, type_data in location_data.items():
                        if 'servers' in type_data:
                            for server_id, server_info in type_data['servers'].items():
                                vpn_id = server_info.get('id')
                                name = server_info.get('friendly_name', 'unknown')
                                location = server_info.get('location', 'unknown')
                                
                                if vpn_id:
                                    try:
                                        # Download UDP config
                                        udp_config = self.download_vpn_config(vpn_id, "udp")
                                        udp_filename = f"{name}_{location}_udp.ovpn"
                                        udp_path = self.vpn_dir / udp_filename
                                        
                                        with open(udp_path, 'wb') as f:
                                            f.write(udp_config)
                                        
                                        # Download TCP config
                                        tcp_config = self.download_vpn_config(vpn_id, "tcp")
                                        tcp_filename = f"{name}_{location}_tcp.ovpn"
                                        tcp_path = self.vpn_dir / tcp_filename
                                        
                                        with open(tcp_path, 'wb') as f:
                                            f.write(tcp_config)
                                        
                                        downloaded.append({
                                            'id': vpn_id,
                                            'name': name,
                                            'location': location,
                                            'udp_file': str(udp_path),
                                            'tcp_file': str(tcp_path)
                                        })
                                        
                                        console.print(f"[green]✓[/green] Downloaded {name} ({location}) - UDP & TCP")
                                        
                                    except Exception as e:
                                        console.print(f"[red]✗[/red] Failed to download {name}: {e}")
        
        return downloaded
    
    def list_vpn_files(self) -> List[Dict[str, Any]]:
        """List downloaded VPN files"""
        vpn_files = []
        
        for file_path in self.vpn_dir.glob("*.ovpn"):
            filename = file_path.name
            parts = filename.replace('.ovpn', '').split('_')
            
            if len(parts) >= 3:
                name = parts[0]
                location = parts[1]
                protocol = parts[2].upper()
                
                vpn_files.append({
                    'filename': filename,
                    'name': name,
                    'location': location,
                    'protocol': protocol,
                    'path': str(file_path)
                })
        
        return vpn_files
    
    def start_vpn(self, vpn_file: str, mode: str = "udp") -> bool:
        """Start VPN connection"""
        try:
            # Find the VPN file
            vpn_path = None
            if os.path.isabs(vpn_file):
                vpn_path = Path(vpn_file)
            else:
                # Search in VPN directory
                for file_path in self.vpn_dir.glob(f"*{vpn_file}*"):
                    if mode.lower() in file_path.name.lower():
                        vpn_path = file_path
                        break
            
            if not vpn_path or not vpn_path.exists():
                console.print(f"[red]Error: VPN file not found for {vpn_file} ({mode})[/red]")
                return False
            
            # Check if openvpn is installed
            try:
                subprocess.run(['openvpn', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                console.print("[red]Error: OpenVPN is not installed or not in PATH[/red]")
                return False
            
            # Start VPN connection
            console.print(f"[yellow]Starting VPN connection: {vpn_path.name}[/yellow]")
            
            # Run openvpn in background
            process = subprocess.Popen([
                'sudo', 'openvpn',
                '--config', str(vpn_path),
                '--daemon'
            ])
            
            if process.returncode == 0:
                console.print(f"[green]✓[/green] VPN connection started successfully")
                return True
            else:
                console.print(f"[red]✗[/red] Failed to start VPN connection")
                return False
                
        except Exception as e:
            console.print(f"[red]Error starting VPN: {e}[/red]")
            return False
    
    def stop_vpn(self) -> bool:
        """Stop VPN connection"""
        try:
            # Find openvpn processes
            result = subprocess.run(['pgrep', 'openvpn'], capture_output=True, text=True)
            
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        subprocess.run(['sudo', 'kill', pid])
                
                console.print("[green]✓[/green] VPN connection stopped")
                return True
            else:
                console.print("[yellow]No active VPN connection found[/yellow]")
                return True
                
        except Exception as e:
            console.print(f"[red]Error stopping VPN: {e}[/red]")
            return False

# Click commands
@click.group()
def vpn():
    """Interact with HackTheBox VPNs"""
    pass



@vpn.command()
def download():
    """Download All VPNs from HackTheBox"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        console.print("[bold blue]Downloading all VPN configurations...[/bold blue]")
        downloaded = vpn_module.download_all_vpns()
        console.print(f"[green]Downloaded {len(downloaded)} VPN configurations[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vpn.command()
def list():
    """List VPNs"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        console.print("[bold blue]Listing VPN servers...[/bold blue]")
        servers = vpn_module.get_vpn_servers()
        
        if servers and isinstance(servers, dict) and 'data' in servers:
            data = servers['data']
            table = Table(title="VPN Servers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Location", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Clients", style="blue")
            table.add_column("Full", style="red")
            
            # Parse the nested structure
            if 'options' in data:
                for location, location_data in data['options'].items():
                    for server_type, type_data in location_data.items():
                        if 'servers' in type_data:
                            for server_id, server_info in type_data['servers'].items():
                                table.add_row(
                                    str(server_info.get('id', 'N/A')),
                                    str(server_info.get('friendly_name', 'N/A')),
                                    str(server_info.get('location', 'N/A')),
                                    str(type_data.get('name', 'N/A')),
                                    str(server_info.get('current_clients', 'N/A')),
                                    "Yes" if server_info.get('full', False) else "No"
                                )
            
            console.print(table)
        else:
            console.print(f"[yellow]No VPN servers found. Response: {servers}[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vpn.command()
@click.argument('vpn_file')
@click.option('--mode', '-m', default='udp', help='Mode (udp/tcp)')
def start(vpn_file, mode):
    """Start a VPN"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        vpn_module.start_vpn(vpn_file, mode)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vpn.command()
def stop():
    """Stop a VPN"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        vpn_module.stop_vpn()
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vpn.command()
def files():
    """List downloaded VPN files"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        console.print("[bold blue]Listing downloaded VPN files...[/bold blue]")
        vpn_files = vpn_module.list_vpn_files()
        
        if vpn_files:
            table = Table(title="Downloaded VPN Files")
            table.add_column("Name", style="cyan")
            table.add_column("Location", style="green")
            table.add_column("Protocol", style="yellow")
            table.add_column("Filename", style="magenta")
            
            for vpn_file in vpn_files:
                table.add_row(
                    vpn_file['name'],
                    vpn_file['location'],
                    vpn_file['protocol'],
                    vpn_file['filename']
                )
            
            console.print(table)
        else:
            console.print("[yellow]No VPN files found. Use 'download' command first.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vpn.command()
def status():
    """Get VPN connection status"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        console.print("[bold blue]VPN Connection Status[/bold blue]")
        status = vpn_module.get_connection_status()
        
        if status and 'data' in status:
            status_data = status['data']
            console.print(Panel.fit(
                f"[bold green]Connection Status[/bold green]\n"
                f"Connected: {status_data.get('connected', 'N/A') or 'N/A'}\n"
                f"Server: {status_data.get('server', 'N/A') or 'N/A'}\n"
                f"IP: {status_data.get('ip', 'N/A') or 'N/A'}\n"
                f"Location: {status_data.get('location', 'N/A') or 'N/A'}",
                title="VPN Status"
            ))
        else:
            console.print("[yellow]No connection status found[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
