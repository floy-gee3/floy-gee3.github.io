## Automating Network Tasks with Python

The Power of Automation:

Manual network configuration and management can be time-consuming and error-prone while hindering scalability. Automation enables the streamlining of repetitive tasks, ensures consistency, and significantly reduces the risk of human errors. Python, with its simplicity and vast library ecosystem, is a fantastic choice for implementing network automation solutions.

Python Scripts for Network Automation:

I've developed a series of Python scripts that leverage the Nornir library to automate a number of network tasks. I've automated the configuration of routing instances and loopback interfaces on multiple devices. Screenshots will highlight the successful application of the configurations.
The configurations were applied on two Juniper SRX devices, vSRX-1 and vSRX-2.

**1. Configuring a loopback interface lo0.0 and a VRF called care-givers into which the loopback interface lo0.0 is then placed:**

[PYTHON CODE FOR ADDING LOOPBACK INTERFACE AND ROUTING-INSTANCE](_posts/add-loopback-and-vrf.py)

This script demonstrates how to configure a VRF and a loopback interface on a Juniper device using Nornir's capabilities. XML was used as the payload type.
First let’s look at the devices before the script was applied. The screenshots below show that there was no routing-instance configured on either device and similarly, no lo0.0 interface.

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/9d9f7ca3-4538-4909-854f-f24089435612)

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/59d5edb5-635b-454b-8ad3-be83779e28f7)

**Results**

I've executed my Python script on actual network devices and captured screenshots of the results. Below are the screenshots that demonstrate the successful outcomes of my automation efforts:
First, a screenshot of the output of the script as it was run in VS Code:

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/02a9695e-d9ff-46eb-b90b-fd1b61641376)

The following shows the devices after the config was applied. The VRF and interface lo0.0 are now configured.

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/d1f26930-dd13-4726-ba47-96e2abdfb3f1)

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/130667c1-3425-4e62-a1ad-fdb2d9485087)

**2. Deleting the loopback interface**

Now that the script for applying the config has been successfully applied, I made another script for deleting the loopback interface:

[PYTHON CODE FOR DELETING LOOPBACK INTERFACE](_posts/delete-loopback.py)

Below is a screenshot showing the script as it was run:

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/e8da7dc0-83ec-40f3-ac96-321a51be22e0)

As can be seen on the devices, the loopback interface lo0.0 has now been deleted on both devices:

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/f6a27c89-1be4-4353-ab7d-93532c749ec2)

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/75ac2141-c4e2-42dc-8c3b-2b0b612c6e94)

**3. Deleting the VRF**

Now let’s delete the residual configuration – i.e. the VRF:

[PYTHON CODE FOR DELETING ROUTING INSTANCE](_posts/delete-vrf.py)

Below is a screenshot of the script as it was being run:

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/77eb6ed8-c962-4fba-af71-77294edc39d8)

A final look at the devices shows that the routing-instance has now also been successfully deleted.

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/c75d057c-4b08-41ae-9fca-4fc70d77a9d2)

![image](https://github.com/floy-gee3/floy-gee3.github.io/assets/26433845/deb4780f-a224-45c2-8ade-7cd34aade0bf)

**Conclusion**

Incorporating automation into network configuration is a game-changer, and Python provides the perfect toolkit for implementing these solutions. By showcasing my Python scripts and the results achieved through automation, I hope to inspire others to embrace automation as an essential skill in modern network engineering.
Whether it's applying IP addresses, configuring routing instances, or tackling more complex network tasks, automation is the key to efficiency, accuracy, and scalability. With a solid foundation in Python and the right libraries like Nornir, anyone can embark on their journey towards becoming a proficient network automation engineer.
So, why wait? Dive into the world of network automation with Python and unlock the potential to transform the way you manage and operate networks.











