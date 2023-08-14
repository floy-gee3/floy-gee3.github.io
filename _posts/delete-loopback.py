import nornir
from nornir_pyez.plugins.tasks import pyez_config, pyez_commit
import os
from nornir import InitNornir
from nornir.core.filter import F
from rich import print
import yaml
import time
from jnpr.junos.exception import LockError  # Import the LockError exception

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/config.yml")

with open('hosts.yml', 'r') as file:
    hosts_data = yaml.safe_load(file)

    for host in hosts_data:
        xml_payload = f"""
            <configuration>
                <interfaces>
                    <interface>
                        <name>{hosts_data[host].get('loopback_interface')}</name>
                            <unit operation="delete">
                                <name>{hosts_data[host].get('loopback_sub-interface')}</name>
                            </unit>
                    </interface>
                </interfaces>
            </configuration>
        """

#first_loading = True

        response = nr.run(
            task=pyez_config, payload=xml_payload, data_format='xml'
        )

# Print the response for each device
        for dev, result in response.items():
            if result.failed:
                print(f"Failed to delete loopback interface {hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')} on {dev}: {result.exception}")
            else:
                print(f"Loopback interface {hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')} deleted successfully on {dev}")

# Perform the commit
        response = nr.run(
            task=pyez_config, payload=xml_payload, data_format='xml'
        )

# Print the response for each device
        for dev, result in response.items():
            if isinstance(result.exception, LockError):
                print(f"LockError encountered on {dev}, retrying after a short delay...")
        # Add a short delay here, e.g., time.sleep(5)
                time.sleep(5)
                response_retry = nr.run(
                    task=pyez_config, payload=xml_payload, data_format='xml'
                )
        # Continue with checking response_retry and printing messages

            elif result.failed:
                print(f"Failed to delete loopback interface {hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')} on {dev}: {result.exception}")
            else:
                print(f"Loopback interface {hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')} deleted successfully on {dev}")

# Check if the commit was successful for all devices

response = nr.run(
    task=pyez_commit, on_failed=True
)

commit_successful = all(result[0].result for result in response.values())

# Print the commit success message if all commits were successful
if commit_successful:
    print("All commits were successful. Way to go dude.")
else:
    print("Commit failed on one or more devices")
