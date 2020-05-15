# Introduction 
ansible playbook to apply base interface and ospf configuration to vSRXes in JCL 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	clone into ~nita on JCL demo host
2.	Software dependencies:
ansible


# Build and Test
1. make sure you can ping vsrx1,2,3
2. run the playbook:
           nita@ubuntu:~/demo1$ ansible-playbook -i hosts site.yml

# Contribute
TODO: 
- refactor to use roles (e.g. build-config, deploy-config)
- add wait_for and use handler to deal with vsrx reload (right now have to run the playbook 2x)
- need to fix hosts inventory file syntax to better differentiate between device types (I.e. so we can do things like 
specify '- hosts: srx' in the playbooks and apply device-specific roles (like nita).
