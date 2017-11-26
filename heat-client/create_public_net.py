'''
Created on Nov 24, 2017

@author: azaringh + lphan
'''
import create_stack
import sys
from pprint import pprint

user_input = sys.argv


if len(user_input) != 4 or user_input[2] =='h':
        print "create_public_net.py <stack-name> <net-name> <subnet 10.1.<dc_number>.x/24>"
        print "Example: python create_public_net.py public-net-stack public-net 10.1.102.0/24"
        exit(1)

#Parse User_input
stack_name = user_input[1]
project_name = 'demo'

net_name = user_input[2] 
subnet_name = net_name+ '-subnet'

ip_prefix = user_input[3]
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

#pprint(StackData['stack_template'])
print ">>> Creating Stack for Network: %s" % (net_name)

stack = create_stack.create_stack(project_name, **StackData)
#print stack
