"""
VPN module for HTB CLI
"""

import os
import subprocess
import click
import glob
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
    
    def get_connections(self) -> Dict[str, Any]:
        """Get current connections status"""
        return self.api.get("/connections")
    
    def switch_vpn_server(self, vpn_id: int) -> Dict[str, Any]:
        """Switch VPN server"""
        return self.api.post(f"/connections/servers/switch/{vpn_id}")
    
    def download_current_vpn(self, product: str = "lab") -> bool:
        """Download VPN config for currently selected server"""
        try:
            # Get current connections to see what server is selected
            connections = self.get_connections()
            
            if not connections or 'data' not in connections:
                console.print("[red]Error: Could not get current connections[/red]")
                return False
            
            data = connections['data']
            
            # Map product names to API keys
            product_map = {
                'lab': 'lab',
                'labs': 'lab',
                'starting_point': 'starting_point',
                'sp': 'starting_point',
                'fortresses': 'fortresses',
                'prolabs': 'pro_labs',
                'competitive': 'competitive'
            }
            
            product_key = product_map.get(product, 'lab')
            
            # Find the assigned server for the specified product
            assigned_server = None
            if product_key in data and data[product_key] and 'assigned_server' in data[product_key]:
                assigned_server = data[product_key]['assigned_server']
            
            if not assigned_server:
                console.print(f"[red]Error: No VPN server currently assigned for {product}[/red]")
                return False
            
            vpn_id = assigned_server.get('id')
            server_name = assigned_server.get('friendly_name', 'unknown')
            location = assigned_server.get('location', 'unknown')
            
            if not vpn_id:
                console.print("[red]Error: No VPN ID found for assigned server[/red]")
                return False
            
            console.print(f"[blue]Downloading VPN for server: {server_name} ({location})[/blue]")
            
            # Download UDP config
            try:
                udp_config = self.api.get_binary(f"/access/ovpnfile/{vpn_id}/0")
                udp_filename = f"{server_name}_{location}_udp.ovpn"
                udp_path = self.vpn_dir / udp_filename
                
                with open(udp_path, 'wb') as f:
                    f.write(udp_config)
                
                console.print(f"[green]✓[/green] Downloaded UDP config: {udp_filename}")
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to download UDP config: {e}")
                return False
            
            # Download TCP config
            try:
                tcp_config = self.api.get_binary(f"/access/ovpnfile/{vpn_id}/0/1")
                tcp_filename = f"{server_name}_{location}_tcp.ovpn"
                tcp_path = self.vpn_dir / tcp_filename
                
                with open(tcp_path, 'wb') as f:
                    f.write(tcp_config)
                
                console.print(f"[green]✓[/green] Downloaded TCP config: {tcp_filename}")
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to download TCP config: {e}")
                return False
            
            console.print(f"[green]✓[/green] Successfully downloaded VPN configs for {server_name}")
            return True
            
        except Exception as e:
            console.print(f"[red]Error downloading VPN: {e}[/red]")
            return False
    
    def switch_to_mode(self, mode: str) -> bool:
        """Switch to a specific mode (labs, sp, fortresses, etc.)"""
        try:
            # Map mode to product and find appropriate server
            mode_map = {
                'labs': 'labs',
                'sp': 'starting_point',
                'fortresses': 'fortresses',
                'prolabs': 'prolabs',
                'endgames': 'endgames',
                'competitive': 'competitive'
            }
            
            product = mode_map.get(mode)
            if not product:
                console.print(f"[red]Invalid mode: {mode}[/red]")
                return False
            
            console.print(f"[blue]Switching to {mode} mode...[/blue]")
            
            # Get servers for this product
            servers = self.get_vpn_servers(product)
            
            if not servers or 'data' not in servers:
                console.print(f"[red]Error: Could not get servers for {product}[/red]")
                return False
            
            data = servers['data']
            
            # Find the first available server
            selected_server = None
            if 'options' in data:
                for location, location_data in data['options'].items():
                    for server_type, type_data in location_data.items():
                        if 'servers' in type_data:
                            for server_id, server_info in type_data['servers'].items():
                                if not server_info.get('full', False):  # Not full
                                    selected_server = server_info
                                    break
                            if selected_server:
                                break
                    if selected_server:
                        break
            
            if not selected_server:
                console.print(f"[red]Error: No available servers found for {mode}[/red]")
                return False
            
            vpn_id = selected_server.get('id')
            server_name = selected_server.get('friendly_name', 'unknown')
            
            if not vpn_id:
                console.print(f"[red]Error: No VPN ID found for {server_name}[/red]")
                return False
            
            console.print(f"[blue]Switching to server: {server_name} (ID: {vpn_id})[/blue]")
            
            # Switch to this server
            result = self.switch_vpn_server(vpn_id)
            
            if result and result.get('status'):
                console.print(f"[green]✓[/green] Successfully switched to {server_name}")
                return True
            else:
                console.print(f"[red]✗[/red] Failed to switch to {server_name}")
                return False
                
        except Exception as e:
            console.print(f"[red]Error switching to {mode}: {e}[/red]")
            return False
    
    def list_vpn_servers(self) -> bool:
        """List VPN servers"""
        try:
            console.print("[bold blue]Listing VPN servers...[/bold blue]")
            servers = self.get_vpn_servers()
            
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
                return True
            else:
                console.print(f"[yellow]No VPN servers found. Response: {servers}[/yellow]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error listing VPN servers: {e}[/red]")
            return False
    
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
    
    def start_vpn(self, filename_pattern: str) -> bool:
        """Start VPN connection based on filename pattern"""
        try:
            # Find matching VPN files
            matching_files = glob.glob(filename_pattern)
            
            if not matching_files:
                console.print(f"[red]No VPN files found matching pattern: {filename_pattern}[/red]")
                return False
            
            # Prefer UDP files over TCP
            udp_files = [f for f in matching_files if 'udp' in f.lower()]
            tcp_files = [f for f in matching_files if 'tcp' in f.lower()]
            
            vpn_file = None
            if udp_files:
                vpn_file = udp_files[0]
                console.print(f"[blue]Using UDP file: {os.path.basename(vpn_file)}[/blue]")
            elif tcp_files:
                vpn_file = tcp_files[0]
                console.print(f"[blue]Using TCP file: {os.path.basename(vpn_file)}[/blue]")
            else:
                vpn_file = matching_files[0]
                console.print(f"[blue]Using file: {os.path.basename(vpn_file)}[/blue]")
            
            # Check if openvpn is installed
            try:
                subprocess.run(['openvpn', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                console.print("[red]Error: OpenVPN is not installed or not in PATH[/red]")
                console.print("[yellow]Please install OpenVPN: sudo pacman -S openvpn[/yellow]")
                return False
            
            # Start VPN connection
            console.print(f"[yellow]Starting VPN connection: {os.path.basename(vpn_file)}[/yellow]")
            
            # Try different methods to start OpenVPN
            success = False
            
            # Method 1: Try with pkexec (GUI password prompt)
            try:
                console.print("[blue]Attempting to start VPN with pkexec...[/blue]")
                process = subprocess.run([
                    'pkexec', 'openvpn',
                    '--config', vpn_file,
                    '--daemon'
                ], capture_output=True, text=True, timeout=10)
                
                if process.returncode == 0:
                    console.print(f"[green]✓[/green] VPN connection started successfully with pkexec")
                    success = True
                else:
                    console.print(f"[yellow]pkexec failed: {process.stderr}[/yellow]")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                console.print("[yellow]pkexec not available or timed out[/yellow]")
            
            # Method 2: Try with sudo (interactive)
            if not success:
                try:
                    console.print("[blue]Attempting to start VPN with sudo...[/blue]")
                    console.print("[yellow]You may be prompted for your password[/yellow]")
                    
                    process = subprocess.run([
                        'sudo', 'openvpn',
                        '--config', vpn_file,
                        '--daemon'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if process.returncode == 0:
                        console.print(f"[green]✓[/green] VPN connection started successfully with sudo")
                        success = True
                    else:
                        console.print(f"[red]sudo failed: {process.stderr}[/red]")
                except subprocess.TimeoutExpired:
                    console.print("[red]sudo command timed out - password prompt may have failed[/red]")
                except Exception as e:
                    console.print(f"[red]sudo error: {e}[/red]")
            
            # Method 3: Try without sudo (if user has permissions)
            if not success:
                try:
                    console.print("[blue]Attempting to start VPN without sudo...[/blue]")
                    process = subprocess.run([
                        'openvpn',
                        '--config', vpn_file,
                        '--daemon'
                    ], capture_output=True, text=True, timeout=10)
                    
                    if process.returncode == 0:
                        console.print(f"[green]✓[/green] VPN connection started successfully without sudo")
                        success = True
                    else:
                        console.print(f"[yellow]Non-sudo failed: {process.stderr}[/yellow]")
                except Exception as e:
                    console.print(f"[red]Non-sudo error: {e}[/red]")
            
            if not success:
                console.print("[red]✗[/red] Failed to start VPN connection")
                console.print("[yellow]Troubleshooting tips:[/yellow]")
                console.print("1. Make sure OpenVPN is installed: sudo pacman -S openvpn")
                console.print("2. Try running manually: sudo openvpn --config <vpn_file>")
                console.print("3. Check if you have sudo privileges")
                console.print("4. Try using pkexec instead of sudo")
                return False
            
            return True
                
        except Exception as e:
            console.print(f"[red]Error starting VPN: {e}[/red]")
            return False
    
    def stop_vpn(self) -> str:
        """Stop VPN connection"""
        try:
            # Find openvpn processes
            result = subprocess.run(['pgrep', 'openvpn'], capture_output=True, text=True)
            
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                console.print(f"[yellow]Found {len(pids)} OpenVPN process(es)[/yellow]")
                
                success = False
                
                # Method 1: Try with pkexec
                try:
                    console.print("[blue]Attempting to stop VPN with pkexec...[/blue]")
                    for pid in pids:
                        if pid:
                            subprocess.run(['pkexec', 'kill', pid], capture_output=True, timeout=5)
                    console.print("[green]✓[/green] VPN connection stopped with pkexec")
                    success = True
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    console.print("[yellow]pkexec not available or timed out[/yellow]")
                
                # Method 2: Try with sudo
                if not success:
                    try:
                        console.print("[blue]Attempting to stop VPN with sudo...[/blue]")
                        for pid in pids:
                            if pid:
                                subprocess.run(['sudo', 'kill', pid], capture_output=True, timeout=10)
                        console.print("[green]✓[/green] VPN connection stopped with sudo")
                        success = True
                    except subprocess.TimeoutExpired:
                        console.print("[red]sudo command timed out - password prompt may have failed[/red]")
                    except Exception as e:
                        console.print(f"[red]sudo error: {e}[/red]")
                
                # Method 3: Try without sudo (if user owns the process)
                if not success:
                    try:
                        console.print("[blue]Attempting to stop VPN without sudo...[/blue]")
                        for pid in pids:
                            if pid:
                                subprocess.run(['kill', pid], capture_output=True, timeout=5)
                        console.print("[green]✓[/green] VPN connection stopped without sudo")
                        success = True
                    except Exception as e:
                        console.print(f"[red]Non-sudo error: {e}[/red]")
                
                if not success:
                    console.print("[red]✗[/red] Failed to stop VPN connection")
                    console.print("[yellow]Try manually: sudo killall openvpn[/yellow]")
                    return "Failed to stop VPN connection"
                
                return "VPN connection stopped successfully"
            else:
                console.print("[yellow]No active VPN connection found[/yellow]")
                return "No active VPN connection found"
                
        except Exception as e:
            console.print(f"[red]Error stopping VPN: {e}[/red]")
            return f"Error stopping VPN: {e}"

# Click command matching Go implementation
@click.command()
@click.option('--download', '-d', is_flag=True, help='Download VPN for currently selected server')
@click.option('--start', is_flag=True, help='Start a VPN')
@click.option('--stop', is_flag=True, help='Stop a VPN')
@click.option('--list', is_flag=True, help='List VPNs')
@click.option('--files', is_flag=True, help='List downloaded VPN files')
@click.option('--switch', is_flag=True, help='Switch VPN server')
@click.option('--mode', '-m', type=click.Choice(['labs', 'sp', 'fortresses', 'prolabs', 'endgames', 'competitive']), help='Mode')
@click.option('--name', '-n', help='VPN name to start (e.g., "EU VIP 7")')
@click.option('--server-id', type=int, help='Server ID to switch to (use with --switch)')
def vpn(download, start, stop, list, files, switch, mode, name, server_id):
    """Interact with HackTheBox VPNs"""
    try:
        api_client = HTBAPIClient()
        vpn_module = VPNModule(api_client)
        
        # Handle list command
        if list:
            vpn_module.list_vpn_servers()
            return
        
        # Handle files command
        if files:
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
                console.print("[yellow]No VPN files found. Use --download command first.[/yellow]")
            return
        
        # Handle switch command
        if switch:
            if not server_id:
                console.print("[red]Server ID is required when using --switch[/red]")
                console.print("[yellow]Use --list to see available server IDs[/yellow]")
                return
            
            console.print(f"[blue]Switching to server ID: {server_id}[/blue]")
            result = vpn_module.switch_vpn_server(server_id)
            
            if result and result.get('status'):
                console.print(f"[green]✓[/green] Successfully switched to server ID {server_id}")
            else:
                console.print(f"[red]✗[/red] Failed to switch to server ID {server_id}")
            return
        
        # Handle download command
        if download:
            console.print("[bold blue]Downloading VPN for currently selected server...[/bold blue]")
            vpn_module.download_current_vpn()
            return
        
        # Handle start and stop commands
        if start and stop:
            console.print("[red]--start and --stop cannot be used at the same time[/red]")
            return
        
        if start:
            if not mode and not name:
                console.print("[red]Either mode (-m) or name (-n) is required when using --start[/red]")
                console.print("[yellow]Available modes: labs - sp - fortresses - prolabs - endgames - competitive[/yellow]")
                console.print("[yellow]Or use --name to specify a VPN name directly[/yellow]")
                return
            
            if name:
                # Start by name directly - find the exact VPN file
                console.print(f"[blue]Starting VPN by name: {name}[/blue]")
                
                # Look for VPN files that match the name exactly
                matching_files = []
                for file_path in vpn_module.vpn_dir.glob("*.ovpn"):
                    if name in file_path.name:
                        matching_files.append(str(file_path))
                
                if not matching_files:
                    console.print(f"[red]No VPN files found matching name: {name}[/red]")
                    console.print("[yellow]Available VPN files:[/yellow]")
                    vpn_files = vpn_module.list_vpn_files()
                    for vpn_file in vpn_files:
                        console.print(f"  - {vpn_file['name']}")
                    return
                
                # Prefer UDP files over TCP
                udp_files = [f for f in matching_files if 'udp' in f.lower()]
                tcp_files = [f for f in matching_files if 'tcp' in f.lower()]
                
                vpn_file = None
                if udp_files:
                    vpn_file = udp_files[0]
                    console.print(f"[blue]Using UDP file: {os.path.basename(vpn_file)}[/blue]")
                elif tcp_files:
                    vpn_file = tcp_files[0]
                    console.print(f"[blue]Using TCP file: {os.path.basename(vpn_file)}[/blue]")
                else:
                    vpn_file = matching_files[0]
                    console.print(f"[blue]Using file: {os.path.basename(vpn_file)}[/blue]")
                
                vpn_module.start_vpn(vpn_file)
            else:
                # Start by mode - use the currently assigned server for that mode
                console.print(f"[blue]Starting VPN for {mode} mode using currently assigned server...[/blue]")
                
                # Get current connections to find the assigned server
                connections = vpn_module.get_connections()
                if not connections or 'data' not in connections:
                    console.print("[red]Could not get current connections[/red]")
                    return
                
                data = connections['data']
                
                # Map mode to product key
                mode_map = {
                    'labs': 'lab',
                    'sp': 'starting_point',
                    'fortresses': 'fortresses',
                    'prolabs': 'pro_labs',
                    'endgames': 'endgames',
                    'competitive': 'competitive'
                }
                
                product_key = mode_map.get(mode, 'lab')
                
                if product_key not in data or not data[product_key] or 'assigned_server' not in data[product_key]:
                    console.print(f"[red]No server assigned for {mode} mode[/red]")
                    return
                
                assigned_server = data[product_key]['assigned_server']
                server_name = assigned_server.get('friendly_name', 'unknown')
                location = assigned_server.get('location', 'unknown')
                
                console.print(f"[blue]Current {mode} server: {server_name} ({location})[/blue]")
                
                # Check if VPN files already exist for this server
                vpn_files = vpn_module.list_vpn_files()
                existing_files = []
                
                for vpn_file in vpn_files:
                    if server_name in vpn_file['name'] and location in vpn_file['location']:
                        existing_files.append(vpn_file['path'])
                
                # If files don't exist, download them
                if not existing_files:
                    console.print(f"[blue]VPN files not found for {server_name}, downloading...[/blue]")
                    if not vpn_module.download_current_vpn(mode):
                        console.print(f"[red]Failed to download VPN for {mode} mode[/red]")
                        return
                    
                    # Re-check for files after download
                    vpn_files = vpn_module.list_vpn_files()
                    existing_files = []
                    
                    for vpn_file in vpn_files:
                        if server_name in vpn_file['name'] and location in vpn_file['location']:
                            existing_files.append(vpn_file['path'])
                else:
                    console.print(f"[blue]VPN files already exist for {server_name}[/blue]")
                
                # Start the VPN with existing files
                if existing_files:
                    # Prefer UDP files over TCP
                    udp_files = [f for f in existing_files if 'udp' in f.lower()]
                    tcp_files = [f for f in existing_files if 'tcp' in f.lower()]
                    
                    vpn_file = None
                    if udp_files:
                        vpn_file = udp_files[0]
                        console.print(f"[blue]Starting VPN with: {os.path.basename(vpn_file)}[/blue]")
                    elif tcp_files:
                        vpn_file = tcp_files[0]
                        console.print(f"[blue]Starting VPN with: {os.path.basename(vpn_file)}[/blue]")
                    else:
                        vpn_file = existing_files[0]
                        console.print(f"[blue]Starting VPN with: {os.path.basename(vpn_file)}[/blue]")
                    
                    vpn_module.start_vpn(vpn_file)
                else:
                    console.print(f"[red]No VPN files found for server: {server_name}[/red]")
            
        elif stop:
            message = vpn_module.stop_vpn()
            console.print(f"[green]{message}[/green]")
            # Note: Discord webhook functionality would need to be implemented separately
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
