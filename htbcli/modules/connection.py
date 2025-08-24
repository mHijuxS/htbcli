"""
Connection module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class ConnectionModule:
    """Module for handling VPN connection-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def resolve_prolab_identifier_to_id(self, identifier: str) -> Optional[int]:
        """Resolve prolab identifier/slug to numeric ID"""
        # Import here to avoid circular imports
        from .prolabs import ProlabsModule
        prolabs_module = ProlabsModule(self.api)
        return prolabs_module.resolve_prolab_identifier_to_id(identifier)
    
    def get_access_ovpnfile_udp(self, vpn_id: int) -> Dict[str, Any]:
        """Download UDP VPN config"""
        return self.api.get(f"/access/ovpnfile/{vpn_id}/0")
    
    def get_access_ovpnfile_tcp(self, vpn_id: int) -> Dict[str, Any]:
        """Download TCP VPN config"""
        return self.api.get(f"/access/ovpnfile/{vpn_id}/0/1")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current active connections"""
        return self.api.get("/connection/status")
    
    def get_connection_status_prolab(self, prolab_id: int) -> Dict[str, Any]:
        """Get VPN server status for prolab"""
        return self.api.get(f"/connection/status/prolab/{prolab_id}")
    
    def get_connection_status_product(self, product_name: str) -> Dict[str, Any]:
        """Get VPN server status for product"""
        return self.api.get(f"/connection/status/{product_name}")
    
    def get_connections(self) -> Dict[str, Any]:
        """Get last set connections"""
        return self.api.get("/connections")
    
    def get_connections_servers(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get list of VPN servers"""
        return self.api.get("/connections/servers", params=params)
    
    def get_connections_servers_prolab(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab VPN servers"""
        return self.api.get(f"/connections/servers/prolab/{prolab_id}")
    
    def switch_vpn_server(self, vpn_id: int) -> Dict[str, Any]:
        """Switch VPN server"""
        return self.api.post(f"/connections/servers/switch/{vpn_id}")

# Click commands
@click.group()
def connection():
    """VPN connection-related commands"""
    pass

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def status(debug, json_output):
    """Get current active connections"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connection_status()
        
        if result and 'data' in result:
            status_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Connection Status[/bold green]\n"
                f"Connected: {status_data.get('connected', 'N/A') or 'N/A'}\n"
                f"Server: {status_data.get('server', 'N/A') or 'N/A'}\n"
                f"IP: {status_data.get('ip', 'N/A') or 'N/A'}\n"
                f"Location: {status_data.get('location', 'N/A') or 'N/A'}",
                title="Connection Status"
            ))
        else:
            console.print("[yellow]No connection status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--product', '-p', type=click.Choice(['competitive', 'labs', 'starting_point', 'fortresses']), 
              default='labs', help='Product type for VPN servers')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def servers(product, debug, json_output):
    """Get list of VPN servers for a specific product"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connections_servers(params={"product": product})
        
        if result and 'data' in result:
            data = result['data']
            
            if debug or json_output:
                handle_debug_option(debug, result, "Debug: VPN Servers", json_output)
                return
            
            table = Table(title=f"VPN Servers - {product.title()}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Location", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Status", style="blue")
            
            if 'options' in data:
                for location, location_data in data['options'].items():
                    for server_type, type_data in location_data.items():
                        if 'servers' in type_data:
                            for server_id, server_info in type_data['servers'].items():
                                status = "Full" if server_info.get('full', False) else "Available"
                                table.add_row(
                                    str(server_id),
                                    str(server_info.get('friendly_name', 'N/A')),
                                    str(location),
                                    str(server_type),
                                    status
                                )
            
            console.print(table)
        else:
            console.print("[yellow]No servers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def connections(debug, json_output):
    """Get last set connections"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connections()
        
        if result and 'data' in result:
            connections_data = result['data']
            
            console.print("[bold blue]Current VPN Server Assignments[/bold blue]")
            
            # Check each product type
            products = {
                'lab': 'Labs',
                'starting_point': 'Starting Point',
                'fortresses': 'Fortresses',
                'pro_labs': 'ProLabs',
                'competitive': 'Competitive'
            }
            
            for product_key, product_name in products.items():
                if product_key in connections_data and connections_data[product_key]:
                    product_data = connections_data[product_key]
                    
                    if 'assigned_server' in product_data and product_data['assigned_server']:
                        server = product_data['assigned_server']
                        console.print(Panel.fit(
                            f"[bold green]{product_name}[/bold green]\n"
                            f"Server: {server.get('friendly_name', 'N/A')}\n"
                            f"Location: {server.get('location', 'N/A')}\n"
                            f"ID: {server.get('id', 'N/A')}\n"
                            f"Can Access: {product_data.get('can_access', 'N/A')}",
                            title=f"{product_name} Assignment"
                        ))
                    else:
                        console.print(f"[yellow]No server assigned for {product_name}[/yellow]")
                else:
                    console.print(f"[yellow]No data for {product_name}[/yellow]")
        else:
            console.print("[yellow]No connections found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('vpn_id', type=int)
def download_udp(vpn_id, debug, json_output):
    """Download UDP VPN config"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_access_ovpnfile_udp(vpn_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]UDP VPN Config Downloaded[/bold green]\n"
                f"VPN ID: {vpn_id}\n"
                f"Protocol: UDP\n"
                f"Status: Success",
                title="VPN Download"
            ))
        else:
            console.print("[yellow]Failed to download VPN config[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('vpn_id', type=int)
def download_tcp(vpn_id, debug, json_output):
    """Download TCP VPN config"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_access_ovpnfile_tcp(vpn_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]TCP VPN Config Downloaded[/bold green]\n"
                f"VPN ID: {vpn_id}\n"
                f"Protocol: TCP\n"
                f"Status: Success",
                title="VPN Download"
            ))
        else:
            console.print("[yellow]Failed to download VPN config[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('vpn_id', type=int)
def switch(vpn_id, debug, json_output):
    """Switch VPN server"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.switch_vpn_server(vpn_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]VPN Server Switch Result[/bold green]\n"
                f"VPN ID: {vpn_id}\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Server Switch"
            ))
        else:
            console.print("[yellow]No result from server switch[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('prolab_identifier')
def prolab_status(prolab_identifier, debug, json_output):
    """Get VPN server status for prolab by name or ID"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        
        # Try to parse as integer first, then resolve as identifier
        try:
            prolab_id = int(prolab_identifier)
        except ValueError:
            # Resolve identifier to ID
            prolab_id = connection_module.resolve_prolab_identifier_to_id(prolab_identifier)
            if prolab_id is None:
                console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
                return
        
        result = connection_module.get_connection_status_prolab(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Status", json_output)
            return
        
        if result and 'data' in result:
            status_data = result['data']
            
            # Extract server information
            server_info = status_data.get('server', {})
            if isinstance(server_info, dict):
                server_name = server_info.get('friendly_name', 'N/A')
                server_hostname = server_info.get('hostname', 'N/A')
                server_id = server_info.get('id', 'N/A')
            else:
                server_name = str(server_info) if server_info else 'N/A'
                server_hostname = 'N/A'
                server_id = 'N/A'
            
            console.print(Panel.fit(
                f"[bold green]ProLab VPN Status[/bold green]\n"
                f"ProLab: {prolab_identifier} (ID: {prolab_id})\n"
                f"Connected: {status_data.get('connected', 'N/A') or 'N/A'}\n"
                f"Server ID: {server_id}\n"
                f"Server Name: {server_name}\n"
                f"Server Hostname: {server_hostname}\n"
                f"IP: {status_data.get('ip', 'N/A') or 'N/A'}",
                title=f"ProLab Status: {prolab_identifier}"
            ))
        else:
            console.print("[yellow]No prolab status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('product_name')
def product_status(product_name, debug, json_output):
    """Get VPN server status for product"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connection_status_product(product_name)
        
        if result and 'data' in result:
            status_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Product VPN Status[/bold green]\n"
                f"Product: {product_name}\n"
                f"Connected: {status_data.get('connected', 'N/A') or 'N/A'}\n"
                f"Server: {status_data.get('server', 'N/A') or 'N/A'}\n"
                f"IP: {status_data.get('ip', 'N/A') or 'N/A'}",
                title="Product Status"
            ))
        else:
            console.print("[yellow]No product status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('prolab_identifier')
def prolab_servers(prolab_identifier, debug, json_output):
    """Get prolab VPN servers by name or ID"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        
        # Try to parse as integer first, then resolve as identifier
        try:
            prolab_id = int(prolab_identifier)
        except ValueError:
            # Resolve identifier to ID
            prolab_id = connection_module.resolve_prolab_identifier_to_id(prolab_identifier)
            if prolab_id is None:
                console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
                return
        
        result = connection_module.get_connections_servers_prolab(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Servers", json_output)
            return
        
        if result and 'data' in result:
            data = result['data']
            
            # Show assigned server
            if 'assigned' in data and data['assigned']:
                assigned = data['assigned']
                console.print(Panel.fit(
                    f"[bold green]Currently Assigned Server[/bold green]\n"
                    f"ProLab: {prolab_identifier} (ID: {prolab_id})\n"
                    f"Server ID: {assigned.get('id', 'N/A') or 'N/A'}\n"
                    f"Server Name: {assigned.get('friendly_name', 'N/A') or 'N/A'}\n"
                    f"Location: {assigned.get('location', 'N/A') or 'N/A'}\n"
                    f"Current Clients: {assigned.get('current_clients', 'N/A') or 'N/A'}",
                    title=f"Assigned Server: {prolab_identifier}"
                ))
            
            # Show available servers
            if 'options' in data and data['options']:
                console.print("\n[bold]Available Servers:[/bold]")
                
                for region, region_data in data['options'].items():
                    for location_name, location_data in region_data.items():
                        console.print(f"\n[cyan]{location_name} ({location_data.get('location', 'N/A')})[/cyan]")
                        
                        servers = location_data.get('servers', {})
                        if servers:
                            table = Table(title=f"Servers in {location_name} - {prolab_identifier}")
                            table.add_column("ID", style="cyan")
                            table.add_column("Name", style="green")
                            table.add_column("Location", style="yellow")
                            table.add_column("Status", style="magenta")
                            table.add_column("Clients", style="blue")
                            
                            for server_id, server in servers.items():
                                status = "Full" if server.get('full') else "Available"
                                table.add_row(
                                    str(server.get('id', 'N/A') or 'N/A'),
                                    str(server.get('friendly_name', 'N/A') or 'N/A'),
                                    str(server.get('location', 'N/A') or 'N/A'),
                                    status,
                                    str(server.get('current_clients', 'N/A') or 'N/A')
                                )
                            
                            console.print(table)
                        else:
                            console.print("[yellow]No servers available in this location[/yellow]")
            else:
                console.print("[yellow]No server options available[/yellow]")
        else:
            console.print("[yellow]No prolab servers data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
