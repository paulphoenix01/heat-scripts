'''
Created on Dec 20, 2017

@author: azaringh + lphan
'''
import create_stack
import sys

user_input = sys.argv


if len(user_input) != 3 or user_input[2] =='h':
        print "create_service_template <stack-name> <template-name>"
	print "Example: python create_service_template.py fw-template-stack firewall"
	exit(1)

project_name = 'appformix'
stack_name = user_input[1]

template_name = user_input[2] + '-service-template'


StackData = { 'stack_name': project_name + '-service-template',
                'yaml_file':'../templates/service_template.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_template.jinja',
                'stack_template': { 
                                   'name': template_name,
                                   'mode': 'in-network',
                                   'type': 'firewall',
                                   'image': 'SDN-NoNAT',
                                   'flavor': 'm1.medium',
                                   'shared_ip_list': 'False,True,True',
                                   'scaling': 'True',
                                   'ordered_interfaces': 'True',
                                   'service_interface_type_list': 'management,left,right'
                                    }
               }

stack = create_stack.create_stack(project_name, **StackData)
 
#print StackData
