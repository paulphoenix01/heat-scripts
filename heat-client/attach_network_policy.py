'''
Created on Nov 25, 2017

@author: azaringh + lphan
'''
import create_stack
import sys 
from pprint import pprint

user_input = sys.argv

config_node_ip = '192.168.250.1'

if len(user_input) != 4 or user_input[2] =='h':
        print "attach_net_policy <stack-name> <net_1_name> <net_2_name>"
        print "Example: python attach_net_policy.py attach-policy-stack demo-vm1-vnet demo-vm2-vnet"
        exit(1)

#Parse User_input
stack_name = user_input[1]
project_name = 'appformix'

net_1_name = "default-domain:%s:%s" %(project_name, user_input[2])
net_2_name = "default-domain:%s:%s" %(project_name, user_input[3])

#Policy_name = "vnet1<->vnet2"
policy_name = user_input[2] + "<->" + user_input[3]

StackData = {   'stack_name': stack_name,
                'yaml_file':'../templates/network_policy.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'network_policy.jinja',
                'stack_template': { 
                                    'policy_name': policy_name,
                                    'direction': '<>',
                                    'action': 'pass',
                                    'start_src_ports': -1,
                                    'end_src_ports': -1,
                                    'start_dst_ports': -1,
                                    'end_dst_ports': -1,
                                    'net_1_name' : net_1_name,
                                    'net_2_name': net_2_name
                                    }
            }

#pprint(StackData)
print ">>> Creating Stack for Attaching Network Policy: %s" %(policy_name)

stack = create_stack.create_stack(project_name, **StackData)
#print stack
