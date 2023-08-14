import os
import nornir
from nornir_pyez.plugins.tasks import pyez_config, pyez_commit
from nornir.core.filter import F
from nornir import InitNornir
from rich import print
import yaml

script_dir = os.path.dirname(os.path.realpath(__file__))

# Initialize commit_response
commit_response = {}

#nr = InitNornir(config_file=f"{script_dir}/config.yml", hosts=f"{script_dir}/hosts.yml")
nr = InitNornir(config_file=f"{script_dir}/config.yml")

# Loop through the devices and apply the respective IP address
with open('hosts.yml', 'r') as file:
    hosts_data = yaml.safe_load(file)
#    print(hosts_data)

    for host in hosts_data:
        xml_payload = f"""
            <configuration>
                <interfaces>
                    <interface>
                        <name>lo0</name>
                            <unit>
                                <name>0</name>
                                <family operation="replace">
                                    <inet>
                                        <address>
                                            <name>{hosts_data[host].get('loopback0.0_address')}</name>
                                        </address>
                                    </inet>
                                </family>
                            </unit>
                    </interface>
                </interfaces>
            </configuration>
        """
        #print(xml_payload)

        first_loading = True

        response = nr.filter(F(name=host)).run(
            task=pyez_config, payload=xml_payload, data_format='xml', first_loading=first_loading
        )

        # Print the response for each device
        for dev, result in response.items():
            if result.failed:
                print(f"Failed to configure interface '{hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')}' and apply IP address on {dev}: {result.exception}")
            else:
                print(f"Interface '{hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')}' and its IP address were configured successfully on {dev}")

        xml_payload = f"""
            <configuration>
                <routing-instances>
                    <instance>
                        <name>{hosts_data[host].get('routing_instance')}</name>
                        <instance-type>vrf</instance-type>
                        <interface>
                            <name>{hosts_data[host].get('loopback_interface')}.{hosts_data[host].get('loopback_sub-interface')}</name>
                        </interface>
                        <vrf-target>
                            <import>target:{hosts_data[host].get('route_target')}</import>
                            <export>target:{hosts_data[host].get('route_target')}</export>
                        </vrf-target>
                        <route-distinguisher>
                            <rd-type>{hosts_data[host].get('route_distinguisher')}</rd-type>
                        </route-distinguisher>
                    </instance>
                </routing-instances>
            </configuration>
        """
        
        first_loading = False

        response = nr.filter(F(name=host)).run(
            task=pyez_config, payload=xml_payload, data_format='xml', first_loading=first_loading
        )
        
        # Print the response for each device
        for dev, result in response.items():
            if result.failed:
                print(f"Failed to configure routing-instance '{hosts_data[host].get('routing_instance')}' on {dev}: {result.exception}")
            else:
                print(f"Routing-instance '{hosts_data[host].get('routing_instance')}' configured successfully on {dev}")

        # Perform the commit
        commit_response = nr.filter(F(name=host)).run(
            task=pyez_commit, on_failed=True
        )

        # Print the response for each device
        for dev, result in commit_response.items():
            if result.failed:
                print(f"Commit failed on {dev}: {result.exception}")
            else:
                print(f"Configuration committed successfully on {dev}")

# Check if the commit was successful for all devices
commit_successful = all(result[0].result for result in commit_response.values())

# Print the commit success message if all commits were successful
if commit_successful:
    print("All commits were successful. Way to go dude.")
else:
    print("Commit failed on one or more devices")
