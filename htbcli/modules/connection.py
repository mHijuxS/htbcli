"""
Connection module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class ConnectionModule:
    """Module for handling VPN connection-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
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
    
    def get_connections_servers(self) -> Dict[str, Any]:
        """Get list of VPN servers"""
        return self.api.get("/connections/servers")
    
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
def status():
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
def servers():
    """Get list of VPN servers"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connections_servers()
        
        if result and 'data' in result:
            servers_data = result['data']
            
            table = Table(title="VPN Servers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Location", style="yellow")
            table.add_column("Status", style="magenta")
            table.add_column("Load", style="blue")
            
            for server in servers_data:
                table.add_row(
                    str(server.get('id', 'N/A') or 'N/A'),
                    str(server.get('name', 'N/A') or 'N/A'),
                    str(server.get('location', 'N/A') or 'N/A'),
                    str(server.get('status', 'N/A') or 'N/A'),
                    str(server.get('load', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No servers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
def connections():
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
@click.argument('vpn_id', type=int)
def download_udp(vpn_id):
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
@click.argument('vpn_id', type=int)
def download_tcp(vpn_id):
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
@click.argument('vpn_id', type=int)
def switch(vpn_id):
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
@click.argument('prolab_id', type=int)
def prolab_status(prolab_id):
    """Get VPN server status for prolab"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connection_status_prolab(prolab_id)
        
        if result and 'data' in result:
            status_data = result['data']
            console.print(Panel.fit(
                f"[bold green]ProLab VPN Status[/bold green]\n"
                f"ProLab ID: {prolab_id}\n"
                f"Connected: {status_data.get('connected', 'N/A') or 'N/A'}\n"
                f"Server: {status_data.get('server', 'N/A') or 'N/A'}\n"
                f"IP: {status_data.get('ip', 'N/A') or 'N/A'}",
                title="ProLab Status"
            ))
        else:
            console.print("[yellow]No prolab status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@connection.command()
@click.argument('product_name')
def product_status(product_name):
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
@click.argument('prolab_id', type=int)
def prolab_servers(prolab_id):
    """Get prolab VPN servers"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connections_servers_prolab(prolab_id)
        
        if result and 'data' in result:
            servers_data = result['data']
            
            table = Table(title=f"ProLab VPN Servers (ID: {prolab_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Location", style="yellow")
            table.add_column("Status", style="magenta")
            table.add_column("Load", style="blue")
            
            for server in servers_data:
                table.add_row(
                    str(server.get('id', 'N/A') or 'N/A'),
                    str(server.get('name', 'N/A') or 'N/A'),
                    str(server.get('location', 'N/A') or 'N/A'),
                    str(server.get('status', 'N/A') or 'N/A'),
                    str(server.get('load', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No prolab servers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
