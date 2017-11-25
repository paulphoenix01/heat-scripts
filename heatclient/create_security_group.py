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
	print "create_security_group <stack_name> <ipam_name>"
	print "Example: python create_security_group.py demo_sg_stack demo_sg"
	exit(1)

stack_name = user_input[1]
sg_name = user_input[2]

StackData = {   'stack_name': stack_name,
                'yaml_file':'../templates/security_group.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'security_group.jinja',
                'stack_template': { 
                                     'sg_name': sg_name
                                    }
            }

stack = create_stack.create_stack(project_name, **StackData)
print stack
