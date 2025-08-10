#!/usr/bin/env python3
"""
Script to analyze and compare HTB API endpoints
"""

import yaml
from collections import defaultdict

def load_swagger_file(filename):
    """Load swagger file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def extract_endpoints_by_tag(swagger_data):
    """Extract all endpoints organized by tag"""
    endpoints_by_tag = defaultdict(list)
    
    for path, methods in swagger_data.get('paths', {}).items():
        for method, details in methods.items():
            if isinstance(details, dict) and 'tags' in details:
                for tag in details['tags']:
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
                    endpoints_by_tag[tag].append(endpoint_info)
    
    return dict(endpoints_by_tag)

def main():
    # Load online swagger
    print("Loading online swagger file...")
    online_swagger = load_swagger_file('swagger_online.yaml')
    
    # Extract endpoints by tag
    online_endpoints = extract_endpoints_by_tag(online_swagger)
    
    print("\n=== ONLINE SWAGGER ENDPOINTS BY TAG ===\n")
    
    for tag, endpoints in sorted(online_endpoints.items()):
        print(f"## {tag} ({len(endpoints)} endpoints)")
        for endpoint in endpoints:
            print(f"  {endpoint['method']} {endpoint['path']} - {endpoint['summary']}")
        print()
    
    # Save to file for reference
    with open('online_endpoints.txt', 'w') as f:
        f.write("=== ONLINE SWAGGER ENDPOINTS BY TAG ===\n\n")
        for tag, endpoints in sorted(online_endpoints.items()):
            f.write(f"## {tag} ({len(endpoints)} endpoints)\n")
            for endpoint in endpoints:
                f.write(f"  {endpoint['method']} {endpoint['path']} - {endpoint['summary']}\n")
            f.write("\n")
    
    print("Endpoints saved to online_endpoints.txt")

if __name__ == "__main__":
    main()
