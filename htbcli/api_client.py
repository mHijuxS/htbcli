"""
API Client for HTB CLI
"""

import requests
from typing import Dict, Any, Optional, Union
from .config import Config

class HTBAPIClient:
    """Main API client for HTB API interactions"""
    
    def __init__(self, version: str = "v4"):
        self.version = version
        self.base_url = Config.BASE_URL_V5 if version == "v5" else Config.BASE_URL_V4
        self.session = requests.Session()
        self.session.headers.update(Config.get_auth_headers())
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to HTB API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data
            )
            
            # Special handling for flag submission - 500 with "Incorrect Flag" is actually a valid response
            if response.status_code == 500 and endpoint == "/machine/own":
                try:
                    response_data = response.json()
                    if "message" in response_data and "Incorrect Flag" in response_data["message"]:
                        return response_data
                except:
                    pass
            
            # Special handling for pwnbox terminate - 404 when no active instance is a valid response
            if response.status_code == 404 and endpoint == "/pwnbox/terminate":
                try:
                    response_data = response.json()
                    return response_data
                except:
                    pass
            
            # Special handling for pwnbox terminate - 204 when successfully terminated (no content)
            if response.status_code == 204 and endpoint == "/pwnbox/terminate":
                return {"message": "PwnBox terminated successfully"}
            
            # Special handling for prolab connection status - 400 when not connected is a valid response
            if response.status_code == 400 and "/connection/status/prolab/" in endpoint:
                try:
                    response_data = response.json()
                    return response_data
                except:
                    pass
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Add more detailed error information
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise Exception(f"API request failed: {e} - Response: {error_detail}")
                except:
                    raise Exception(f"API request failed: {e} - Status: {e.response.status_code} - Response: {e.response.text}")
            else:
                raise Exception(f"API request failed: {e}")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request"""
        return self._make_request("POST", endpoint, data=data, json_data=json_data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self._make_request("PUT", endpoint, data=data, json_data=json_data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request("DELETE", endpoint)
    
    def get_binary(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> bytes:
        """Make GET request and return binary data"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method="GET",
                url=url,
                params=params
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
