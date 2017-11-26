'''
Created on Nov 24, 2017

@author: azaringh
'''
import create_stack
import sys
from pprint import pprint

user_input = sys.argv

config_node_ip = '192.168.250.1'

print user_input

if len(user_input) != 4 or user_input[2] =='h':
        print "assign_floating.py <stack-name> <public_net_name || id> <port_id> <public-ip-subnet>"
        print "Example: python assign_floating.py assign-floating-stack public-net-3 c3a0ceab-71f0-422b-8b3e-77d7581d69c2 10.1.192.0/24"
        exit(1)

#Parse User_input
stack_name = user_input[1]
project_name = 'demo'

network = user_input[4].split('/')
floating_ip_pool_subnet_prefix = network[0]
floating_ip_pool_subnet_prefix_len = network[1]

virtual_network = user_input[2] 
port_id = user_input[3]


StackData = { 'stack_name': stack_name,                
               'yaml_file':'../templates/assign_floating.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'assign_floating.jinja',
                 'stack_template': {
					 'virtual_network' : virtual_network,
					 'floating_ip_pool_subnet_prefix': floating_ip_pool_subnet_prefix,
					 'floating_ip_pool_subnet_prefix_len': floating_ip_pool_subnet_prefix_len
                                         'port_id': port_id
                                         }
                }

pprint(StackData['stack_template'])

stack = create_stack.create_stack(project_name, **StackData)
print stack
