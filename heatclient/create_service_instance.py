'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.10.156'
project_name = 'zeppo'

StackData = { 'stack_name': project_name + '-service-instance',
                'yaml_file':'../templates/service_instance.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_instance.jinja',
                'stack_template': { 
                                   'instance_name': project_name + '-service-instance',
                                   'template': 'default-domain:' + project_name + '-service-template',
                                   'net_1_name': 'default-domain:' + project_name + ':' + project_name + '-vnet-1',
                                   'net_2_name': 'default-domain:' + project_name + ':' + project_name + '-vnet-2',
                                   'max_instances': 2
                                    }
               }

stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack