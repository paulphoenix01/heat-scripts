'''
Created on Nov 24, 2017

@author: azaringh
'''
import create_stack
import sys
from pprint import pprint

user_input = sys.argv

config_node_ip = '192.168.250.1'

if len(user_input) != 5 or user_input[2] =='h':
        print "create_public_vn <stack-name> <tenant-name> <net-name> <subnet x.x.x.x/24>"
        print "Example: python create_vm.py create-vm1-stack demo demo-vm1 192.168.1.0/24"
	print "Example python create_vm.py create-vm2-stack demo demo-vm2 192.168.2.0/24"
        exit(1)

#Parse User_input
stack_name = user_input[1]
project_name = user_input[2]

net_name = user_input[3] 
subnet_name = user_input[3] + 'subnet'

ip_prefix = user_input[4]
default_gateway = ip_prefix.replace('.0/24', '.1')

ipam_name = project_name + '-ipam'
route_targets='65250:10250'


StackData = { 'stack_name': stack_name,                
               'yaml_file':'../templates/public_vn.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'public_vn.jinja',
                 'stack_template': {
                                         'net_name' : net_name,
					 'subnet_name': subnet_name,
					 'ip_prefix': ip_prefix,
					 'default_gateway' : default_gateway,
					 'ipam_name' : ipam_name,
                                         'route_targets': route_targets
                                         }
                }

pprint(StackData['stack_template'])

stack = create_stack.create_stack(project_name, **StackData)
print stack
