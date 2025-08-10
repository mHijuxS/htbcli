"""
Swagger/OpenAPI Parser for HTB CLI
"""

import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path

class SwaggerParser:
    """Parser for HTB OpenAPI specification"""
    
    def __init__(self, swagger_file: str = "swagger.htb"):
        self.swagger_file = Path(swagger_file)
        self.spec = self._load_spec()
    
    def _load_spec(self) -> Dict[str, Any]:
        """Load OpenAPI specification from file"""
        if not self.swagger_file.exists():
            raise FileNotFoundError(f"Swagger file not found: {self.swagger_file}")
        
        with open(self.swagger_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_tags(self) -> List[Dict[str, str]]:
        """Get all available tags/modules"""
        return self.spec.get('tags', [])
    
    def get_endpoints_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Get all endpoints for a specific tag"""
        endpoints = []
        
        for path, methods in self.spec.get('paths', {}).items():
            for method, details in methods.items():
                if isinstance(details, dict) and 'tags' in details:
                    if tag in details['tags']:
                        endpoint_info = {
                            'path': path,
                            'method': method.upper(),
                            'summary': details.get('summary', ''),
                            'description': details.get('description', ''),
                            'operation_id': details.get('operationId', ''),
                            'parameters': details.get('parameters', []),
                            'request_body': details.get('requestBody'),
                            'responses': details.get('responses', {})
                        }
                        endpoints.append(endpoint_info)
        
        return endpoints
    
    def get_all_endpoints(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all endpoints organized by tag"""
        endpoints_by_tag = {}
        
        for tag_info in self.get_tags():
            tag_name = tag_info['name']
            endpoints_by_tag[tag_name] = self.get_endpoints_by_tag(tag_name)
        
        return endpoints_by_tag
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get all parameter definitions"""
        return self.spec.get('components', {}).get('parameters', {})
    
    def get_schemas(self) -> Dict[str, Any]:
        """Get all schema definitions"""
        return self.spec.get('components', {}).get('schemas', {})
    
    def get_responses(self) -> Dict[str, Any]:
        """Get all response definitions"""
        return self.spec.get('components', {}).get('responses', {})
