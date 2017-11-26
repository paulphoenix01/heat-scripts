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
        print "create_vm <stack-name> <tenant-name> <vm-name> <subnet x.x.x.x/24>"
        print "Example: python create_vm.py create-vm1-stack demo demo-vm1 192.168.1.0/24"
	print "Example: python create_public_net.py public-net-stack demo public-net 10.10.1.0/24"
        exit(1)

#Parse User_input
stack_name = user_input[1]
project_name = user_input[2]
network = user_input[4].split('/')

#Network name/subnet
private_net_1_name = user_input[3]
private_net_1_prefix = network[0]
private_net_1_prefix_len = network[1]

route_target_1 = "target:65250:10250"

StackData = { 'stack_name': stack_name,                
               'yaml_file':'../templates/public_net.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'public_net.jinja',
                 'stack_template': {
                                         'private_net_1_name' : private_net_1_name,
                                         'private_net_1_prefix': private_net_1_prefix,
                                         'private_net_1_prefix_len' : private_net_1_prefix_len,
                                         'route_target_1' : route_target_1
					 }
                }

#pprint(StackData)
stack = create_stack.create_stack(project_name, **StackData)
print stack
