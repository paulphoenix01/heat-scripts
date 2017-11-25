'''
Created on Nov 20, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.13.103'
project_name = 'chico'

StackData = { 'stack_name': project_name + '-service-template',
                'yaml_file':'../templates/service_template.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_template.jinja',
                'stack_template': { 
                                   'name': project_name + '-service-template',
                                   'mode': 'in-network',
                                   'type': 'firewall',
                                   'image': 'service1-firewall',
                                   'flavor': 'm1.medium',
                                   'shared_ip_list': 'False,True,True',
                                   'scaling': 'True',
                                   'ordered_interfaces': 'True',
                                   'service_interface_type_list': 'management,left,right'
                                    }
               }

stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack