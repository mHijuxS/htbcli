#!/usr/bin/env python3
"""
Script to systematically check and fix all HTB CLI modules
"""

import yaml
import os
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

def analyze_module_file(module_name, module_file_path):
    """Analyze a module file to see what endpoints it implements"""
    if not os.path.exists(module_file_path):
        return {"exists": False, "endpoints": []}
    
    with open(module_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract API calls from the file
    endpoints = []
    lines = content.split('\n')
    for line in lines:
        if 'self.api.get(' in line or 'self.api.post(' in line or 'self.api.put(' in line or 'self.api.delete(' in line:
            # Extract the endpoint path
            if 'self.api.get(' in line:
                method = 'GET'
            elif 'self.api.post(' in line:
                method = 'POST'
            elif 'self.api.put(' in line:
                method = 'PUT'
            elif 'self.api.delete(' in line:
                method = 'DELETE'
            else:
                continue
            
            # Extract the path
            start = line.find('self.api.get(') or line.find('self.api.post(') or line.find('self.api.put(') or line.find('self.api.delete(')
            if start != -1:
                start = line.find('(', start) + 1
                end = line.find(')', start)
                if end != -1:
                    path = line[start:end].strip().strip('"\'')
                    if path.startswith('/'):
                        endpoints.append({
                            'path': path,
                            'method': method,
                            'summary': 'Implemented in code'
                        })
    
    return {"exists": True, "endpoints": endpoints}

def main():
    # Load online swagger
    print("Loading online swagger file...")
    online_swagger = load_swagger_file('swagger_online.yaml')
    
    # Extract endpoints by tag
    online_endpoints = extract_endpoints_by_tag(online_swagger)
    
    # Module mapping (swagger tag -> module file)
    module_mapping = {
        'Badges': 'htbcli/modules/badges.py',
        'Career': 'htbcli/modules/career.py',
        'Challenges': 'htbcli/modules/challenges.py',
        'Connection': 'htbcli/modules/connection.py',
        'Fortresses': 'htbcli/modules/fortresses.py',
        'Home': 'htbcli/modules/home.py',
        'Machines': 'htbcli/modules/machines.py',
        'Platform': 'htbcli/modules/platform.py',
        'Prolabs': 'htbcli/modules/prolabs.py',
        'PwnBox': 'htbcli/modules/pwnbox.py',
        'Ranking': 'htbcli/modules/ranking.py',
        'Review': 'htbcli/modules/review.py',
        'Season': 'htbcli/modules/season.py',
        'Sherlocks': 'htbcli/modules/sherlocks.py',
        'Starting Point': 'htbcli/modules/starting_point.py',
        'Team': 'htbcli/modules/team.py',
        'Tracks': 'htbcli/modules/tracks.py',
        'Universities': 'htbcli/modules/universities.py',
        'User': 'htbcli/modules/user.py',
        'VM': 'htbcli/modules/vm.py'
    }
    
    print("\n=== MODULE ANALYSIS ===\n")
    
    issues_found = []
    
    for tag, endpoints in sorted(online_endpoints.items()):
        print(f"## {tag} ({len(endpoints)} endpoints)")
        
        # Check if module exists
        module_file = module_mapping.get(tag)
        if not module_file:
            print(f"  ❌ No module file mapped for tag '{tag}'")
            issues_found.append(f"Missing module mapping for {tag}")
            continue
        
        # Analyze module file
        module_analysis = analyze_module_file(tag, module_file)
        
        if not module_analysis["exists"]:
            print(f"  ❌ Module file does not exist: {module_file}")
            issues_found.append(f"Missing module file: {module_file}")
            continue
        
        # Compare endpoints
        implemented_endpoints = {ep['path']: ep for ep in module_analysis["endpoints"]}
        online_endpoint_paths = {ep['path'] for ep in endpoints}
        
        missing_endpoints = online_endpoint_paths - set(implemented_endpoints.keys())
        extra_endpoints = set(implemented_endpoints.keys()) - online_endpoint_paths
        
        if missing_endpoints:
            print(f"  ⚠️  Missing endpoints ({len(missing_endpoints)}):")
            for endpoint in sorted(missing_endpoints):
                print(f"    - {endpoint}")
            issues_found.append(f"{tag}: Missing {len(missing_endpoints)} endpoints")
        
        if extra_endpoints:
            print(f"  ⚠️  Extra endpoints ({len(extra_endpoints)}):")
            for endpoint in sorted(extra_endpoints):
                print(f"    - {endpoint}")
            issues_found.append(f"{tag}: {len(extra_endpoints)} extra endpoints")
        
        if not missing_endpoints and not extra_endpoints:
            print(f"  ✅ All endpoints correctly implemented")
        
        print()
    
    # Summary
    print("=== SUMMARY ===")
    if issues_found:
        print(f"Found {len(issues_found)} issues:")
        for issue in issues_found:
            print(f"  - {issue}")
    else:
        print("✅ All modules are correctly implemented!")
    
    # Save detailed report
    with open('module_analysis_report.txt', 'w') as f:
        f.write("=== HTB CLI MODULE ANALYSIS REPORT ===\n\n")
        for tag, endpoints in sorted(online_endpoints.items()):
            f.write(f"## {tag} ({len(endpoints)} endpoints)\n")
            for endpoint in endpoints:
                f.write(f"  {endpoint['method']} {endpoint['path']} - {endpoint['summary']}\n")
            f.write("\n")
    
    print(f"\nDetailed report saved to module_analysis_report.txt")

if __name__ == "__main__":
    main()
