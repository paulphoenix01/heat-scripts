'''
Created on Nov 23, 2015

@author: azaringh
'''
import create_stack
import sys

user_input = sys.argv

if len(user_input) != 5 or user_input[2] =='h':
        print "create_service_policy <stack-name> <instance-name> <vnet-1-name> <vnet-2-name>"
	print "Example: python create_service_policy.py fw-policy-stack firewall-service-instance demo-vm1-vnet demo-vm2-vnet"
	exit(1)

project_name = 'appformix'
stack_name = user_input[1]

instance_name = user_input[2]
policy_name = instance_name + '-policy'

service_instance_name = 'default-domain:' + project_name + ':' + instance_name
net_1_name = 'default-domain:' + project_name + ':' + user_input[3]
net_2_name = 'default-domain:' + project_name + ':' + user_input[4]

StackData = {   'stack_name': stack_name,
                'yaml_file':'../templates/service_policy.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_policy.jinja',
                'stack_template': { 
                                    'policy_name': policy_name,
                                    'service_instance_name': service_instance_name,
                                    'net_1_name': net_1_name,
                                    'net_2_name': net_2_name
                                    }
            }
stack = create_stack.create_stack(project_name, **StackData)
 
#print stack
