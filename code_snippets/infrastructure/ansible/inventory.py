#!/usr/bin/env python3

import os
import sys
import json
import subprocess

# Configuration
K8S_MASTER_COUNT = 5  # Number of Kubernetes master nodes

# Get MAAS API credentials from environment variables
MAAS_API_URL = os.getenv('MAAS_API_URL', 'http://<maas-ip>:5240/MAAS')
MAAS_API_KEY = os.getenv('MAAS_API_KEY', 'maas-api-key')

# Function to run MAAS CLI commands and get machine information
def get_machines():
    try:
        # Command to get all machines from MAAS
        command = f"maas <profile-name> machines read"
        result = subprocess.check_output(command, shell=True)
        return json.loads(result)  # Parse JSON result
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Function to organize machines into Kubernetes masters, and workers
def organize_inventory(machines):
    # Sort machines by their first IP address
    machines = sorted(machines, key=lambda x: x['ip_addresses'][0])

    inventory = {
        "master": {"hosts": []},
        "worker": {"hosts": []},
        "_meta": {"hostvars": {}}
    }

    # Assign machines to different groups
    for i, machine in enumerate(machines):
        hostname = machine['hostname']
        ip_address = machine['ip_addresses'][0]

        # Add host details
        inventory['_meta']['hostvars'][hostname] = {
            "ansible_host": ip_address
        }

        if i < K8S_MASTER_COUNT:
            inventory['masters']['hosts'].append(hostname)
        else:
            inventory['workers']['hosts'].append(hostname)

    return inventory

# Main function to output inventory in JSON format
def main():
        machines = get_machines()
        inventory = organize_inventory(machines)
        print(json.dumps(inventory, indent=2))

if __name__ == '__main__':
    main()
