#!/usr/bin/env python3
"""
Script to check for deviations between the current network state (snapshots) and the intended state.
"""

import json
import os
import sys
from pathlib import Path


def parse_running_config(config_text):
    """Parse the running config to extract relevant information."""
    lines = config_text.split('\n')
    
    # Extract hostname
    hostname = None
    for line in lines:
        if line.startswith('hostname '):
            hostname = line.split(' ', 1)[1].strip()
            break
    
    # Extract OSPF configuration
    ospf_config = {}
    ospf_section = False
    current_process_id = None
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('router ospf'):
            parts = line.split()
            if len(parts) >= 3:
                current_process_id = int(parts[2])
                ospf_config[current_process_id] = {
                    'router_id': None,
                    'networks': [],
                    'areas': {}
                }
                ospf_section = True
        elif ospf_section and line.startswith('router-id'):
            if current_process_id:
                ospf_config[current_process_id]['router_id'] = line.split(' ', 1)[1].strip()
        elif ospf_section and line.startswith('network'):
            if current_process_id:
                parts = line.split()
                if len(parts) >= 4:  # network X.X.X.X X.X.X.X area X.X.X.X (with wildcard mask) or network X.X.X.X/XX area X.X.X.X (with CIDR)
                    network_part = parts[1]
                    area_part = parts[-1]  # The last part should be the area
                    
                    # Handle both CIDR notation (X.X.X.X/XX) and wildcard mask (X.X.X.X X.X.X.X)
                    if '/' in network_part:  # CIDR notation
                        network = network_part
                    else:  # Wildcard mask notation, convert to CIDR
                        network_ip = network_part
                        wildcard = parts[2]
                        # Convert wildcard to CIDR notation
                        network = wildcard_to_cidr(network_ip, wildcard)
                    
                    if 'networks' not in ospf_config[current_process_id]:
                        ospf_config[current_process_id]['networks'] = []
                    ospf_config[current_process_id]['networks'].append(network)
                    
                    if area_part not in ospf_config[current_process_id]['areas']:
                        ospf_config[current_process_id]['areas'][area_part] = []
                    if network not in ospf_config[current_process_id]['areas'][area_part]:
                        ospf_config[current_process_id]['areas'][area_part].append(network)
        elif line.startswith('!') or line == '':
            continue
        elif ospf_section and (line.startswith('exit') or line.startswith('end')):
            ospf_section = False
            current_process_id = None
        elif ospf_section and line.startswith('area'):
            # Parse area configuration like "area 0.0.0.2 stub no-summary"
            parts = line.split()
            if len(parts) >= 2:
                area_id = parts[1]
                if current_process_id and area_id not in ospf_config[current_process_id]['areas']:
                    ospf_config[current_process_id]['areas'][area_id] = []
    
    # Extract EIGRP configuration
    eigrp_config = {}
    eigrp_section = False
    current_as = None
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('router eigrp'):
            parts = line.split()
            if len(parts) >= 3:
                current_as = int(parts[2])
                eigrp_config[current_as] = {
                    'networks': []
                }
                eigrp_section = True
        elif eigrp_section and line.startswith('network'):
            if current_as:
                parts = line.split()
                if len(parts) >= 2:
                    network_part = parts[1]
                    # Check if there's a wildcard mask (format: network X.X.X.X X.X.X.X)
                    if len(parts) >= 3:
                        wildcard = parts[2]
                        network = wildcard_to_cidr(network_part, wildcard)
                    else:
                        # Assume it's already in CIDR format
                        network = network_part
                    eigrp_config[current_as]['networks'].append(network)
        elif line.startswith('!') or line == '':
            continue
        elif eigrp_section and (line.startswith('exit') or line.startswith('end')):
            eigrp_section = False
            current_as = None
    
    return {
        'hostname': hostname,
        'ospf': ospf_config,
        'eigrp': eigrp_config
    }


def wildcard_to_cidr(ip, wildcard):
    """Convert IP with wildcard mask to CIDR notation."""
    # Convert wildcard to subnet mask first
    wildcard_octets = wildcard.split('.')
    subnet_octets = []
    
    for w_octet in wildcard_octets:
        subnet_octet = 255 - int(w_octet)
        subnet_octets.append(str(subnet_octet))
    
    subnet_mask = '.'.join(subnet_octets)
    
    # Convert subnet mask to CIDR
    cidr = 0
    for octet in subnet_octets:
        binary_octet = bin(int(octet))[2:].zfill(8)
        cidr += binary_octet.count('1')
    
    # Extract network portion of IP based on subnet mask
    ip_octets = ip.split('.')
    network_octets = []
    
    for i in range(4):
        network_octet = int(ip_octets[i]) & int(subnet_octets[i])
        network_octets.append(str(network_octet))
    
    network_ip = '.'.join(network_octets)
    
    return f"{network_ip}/{cidr}"


def check_deviation(snapshot_dir, intent_file):
    """Check for deviations between snapshots and intent."""
    # Load the intended state
    with open(intent_file, 'r') as f:
        intent = json.load(f)
    
    # Find the latest snapshot directories
    snapshot_path = Path(snapshot_dir)
    if not snapshot_path.exists():
        print(f"Snapshot directory {snapshot_dir} does not exist.")
        return
    
    # Get all device directories in the snapshot
    device_dirs = [d for d in snapshot_path.iterdir() if d.is_dir()]
    
    deviations = {}
    
    for device_dir in device_dirs:
        device_name = device_dir.name
        
        if device_name not in intent['routers']:
            print(f"Warning: Device {device_name} found in snapshots but not in intent")
            continue
            
        # Read the running config
        running_config_file = device_dir / "running_config.txt"
        if not running_config_file.exists():
            print(f"Warning: No running_config.txt found for {device_name}")
            continue
            
        with open(running_config_file, 'r') as f:
            config_text = f.read()
            
        parsed_config = parse_running_config(config_text)
        
        # Compare hostname
        intent_hostname = intent['routers'][device_name]['hostname']['name']
        actual_hostname = parsed_config['hostname']
        
        if intent_hostname != actual_hostname:
            if device_name not in deviations:
                deviations[device_name] = []
            deviations[device_name].append(f"Hostname mismatch: intended '{intent_hostname}', actual '{actual_hostname}'")
        
        # Compare OSPF configuration
        if 'ospf' in intent['routers'][device_name]:
            intent_ospf = intent['routers'][device_name]['ospf']
            actual_ospf = parsed_config['ospf']
            
            # Check if OSPF process exists
            if intent_ospf['process_id'] not in actual_ospf:
                if device_name not in deviations:
                    deviations[device_name] = []
                deviations[device_name].append(f"OSPF process {intent_ospf['process_id']} not found in actual config")
            else:
                # Check router ID
                if actual_ospf[intent_ospf['process_id']]['router_id'] != intent_ospf['router_id']:
                    if device_name not in deviations:
                        deviations[device_name] = []
                    deviations[device_name].append(f"OSPF router-id mismatch: intended '{intent_ospf['router_id']}', actual '{actual_ospf[intent_ospf['process_id']]['router_id']}'")
                
                # Check areas and networks
                intent_areas = intent_ospf['areas']
                actual_areas = actual_ospf[intent_ospf['process_id']]['areas']
                
                for area_id, networks in intent_areas.items():
                    # Handle both dotted decimal (0.0.0.x) and integer (x) area representations
                    area_found = False
                    actual_area_key = None
                    
                    # Check if the exact area ID exists
                    if area_id in actual_areas:
                        area_found = True
                        actual_area_key = area_id
                    else:
                        # Convert dotted decimal to integer if needed (e.g., "0.0.0.2" to "2")
                        if '.' in area_id:
                            try:
                                parts = area_id.split('.')
                                if len(parts) == 4 and all(p.isdigit() for p in parts):
                                    # Convert dotted decimal to integer
                                    decimal_area = int(parts[3])  # For simple cases like 0.0.0.2
                                    decimal_area_str = str(decimal_area)
                                    if decimal_area_str in actual_areas:
                                        area_found = True
                                        actual_area_key = decimal_area_str
                            except:
                                pass
                        
                        # Also check the reverse (integer to dotted decimal)
                        elif area_id.isdigit():
                            try:
                                decimal_area = int(area_id)
                                dotted_area = f"0.0.0.{decimal_area}"
                                if dotted_area in actual_areas:
                                    area_found = True
                                    actual_area_key = dotted_area
                            except:
                                pass
                    
                    if not area_found:
                        if device_name not in deviations:
                            deviations[device_name] = []
                        deviations[device_name].append(f"OSPF area {area_id} not found in actual config")
                    else:
                        # Check if all intended networks are in the actual config
                        for network in networks:
                            if network not in actual_areas[actual_area_key]:
                                if device_name not in deviations:
                                    deviations[device_name] = []
                                deviations[device_name].append(f"Network {network} not found in OSPF area {area_id}")
                        
                        # Check if there are extra networks in actual config
                        for network in actual_areas[actual_area_key]:
                            if network not in networks:
                                if device_name not in deviations:
                                    deviations[device_name] = []
                                deviations[device_name].append(f"Extra network {network} found in OSPF area {area_id}")
        
        # Compare EIGRP configuration
        if 'eigrp' in intent['routers'][device_name]:
            intent_eigrp = intent['routers'][device_name]['eigrp']
            actual_eigrp = parsed_config['eigrp']
            
            # Check if EIGRP process exists
            if intent_eigrp['as_number'] not in actual_eigrp:
                if device_name not in deviations:
                    deviations[device_name] = []
                deviations[device_name].append(f"EIGRP AS {intent_eigrp['as_number']} not found in actual config")
            else:
                # Check networks
                intent_networks = set(intent_eigrp['networks'])
                actual_networks = set(actual_eigrp[intent_eigrp['as_number']]['networks'])
                
                missing_networks = intent_networks - actual_networks
                extra_networks = actual_networks - intent_networks
                
                for network in missing_networks:
                    if device_name not in deviations:
                        deviations[device_name] = []
                    deviations[device_name].append(f"EIGRP network {network} missing from actual config")
                
                for network in extra_networks:
                    if device_name not in deviations:
                        deviations[device_name] = []
                    deviations[device_name].append(f"Extra EIGRP network {network} found in actual config")
    
    # Print deviations
    if deviations:
        print("\nDeviations found:")
        print("="*50)
        for device, dev_list in deviations.items():
            print(f"\n{device}:")
            for dev in dev_list:
                print(f"  - {dev}")
    else:
        print("\nNo deviations found. Network state matches intended state.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_deviation.py <snapshot_directory> <intent_file>")
        sys.exit(1)
    
    snapshot_dir = sys.argv[1]
    intent_file = sys.argv[2]
    
    check_deviation(snapshot_dir, intent_file)