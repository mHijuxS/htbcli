"""
API Client for HTB CLI
"""

import requests
from typing import Dict, Any, Optional, Union
from .config import Config

class HTBAPIClient:
    """Main API client for HTB API interactions"""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
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
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
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
