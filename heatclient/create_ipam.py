'''
Created on Nov 24, 2017

@author: azaringh
'''
import create_stack
import sys

user_input = sys.argv

config_node_ip = '192.168.250.1'
project_name = 'demo'
if len(user_input) != 3 or user_input[2] =='h':	
	print "create_ipam <stack_name> <ipam_name>"
	print "Example: python create_ipam demo_ipam_stack demo-ipam"
	exit(1)

stack_name = user_input[1]
ipam_name = user_input[2]

StackData = {   'stack_name': stack_name,
                'yaml_file':'../templates/ipam.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'ipam.jinja',
                'stack_template': { 
                                     'ipam_name': ipam_name
                                    }
            }

stack = create_stack.create_stack(project_name, **StackData)
print stack
