'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack
import sys

user_input = sys.argv


if len(user_input) != 6 or user_input[2] =='h':
        print "create_service_instance <stack-name> <template-name> <instance_name> <vnet-1-name> <vnet-2-name>"
	print "Example: python create_service_instance.py fw-instance-stack firewall firewall demo-vm1-vnet demo-vm2-vnet"
	exit(1)

project_name = 'appformix'
stack_name = user_input[1]

template_name = user_input[2] + '-service-template'
instance_name = user_input[3] + '-service-instance'

net_1_name = user_input[4]
net_2_name = user_input[5]

StackData = { 'stack_name': stack_name,
                'yaml_file':'../templates/service_instance.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_instance.jinja',
                'stack_template': { 
                                   'instance_name': instance_name,
                                   'template': 'default-domain:' + template_name,
                                   'net_1_name': 'default-domain:' + project_name + ':' + net_1_name,
                                   'net_2_name': 'default-domain:' + project_name + ':' + net_2_name,
                                   'max_instances': 2
                                    }
               }

stack = create_stack.create_stack(project_name, **StackData)
 
#print stack
