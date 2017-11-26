'''
Created on Nov 24, 2017

@author: azaringh
'''
import create_stack
import sys
from pprint import pprint

user_input = sys.argv


if len(user_input) != 4 or user_input[2] =='h':
        print "create_vm <stack-name> <vm-name> <subnet x.x.x.x/24>"
        print "Example: python create_vm.py create-vm1-stack demo-vm1 192.168.1.0/24"
	print "Example: python create_vm.py create-vm2-stack demo-vm2 192.168.2.0/24"
        exit(1)

#Parse User_input
stack_name = user_input[1]
#project_name = user_input[2]
project_name = 'demo'
vm_name = user_input[2]
network = user_input[3].split('/')

#Network name/subnet
private_net_name = vm_name + '-vnet'
private_network_prefix = network[0]
private_network_prefix_len = network[1]

port_name_1 = vm_name + '-port'
addr_from_start_true = "True"
sg_name = vm_name + '-sg'


StackData = { 'stack_name': stack_name,                
               'yaml_file':'../templates/deploy_vm_v3.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'deploy_vm_v3.jinja',
                 'stack_template': {
                                         'private_net_name' : private_net_name,
                                         'private_network_prefix': private_network_prefix,
                                         'private_network_prefix_len' : private_network_prefix_len,
                                         'addr_from_start_true': addr_from_start_true,
					 'port_name_1': port_name_1,
					 'sg_name' : sg_name,
					 'server_name': vm_name,
                                         'image': 'ubuntu-stress-test',
                                         'flavor': 'm1.medium'
                                         }
                }

#pprint(StackData)
print ">>> Creating VM stack:  %s" % (vm_name)

stack = create_stack.create_stack(project_name, **StackData)
print stack
