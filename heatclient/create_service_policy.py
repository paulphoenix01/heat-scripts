'''
Created on Nov 23, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.13.103'
project_name = 'chico'

StackData = {   'stack_name': project_name + '-service-policy',
                'yaml_file':'../templates/service_policy.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_policy.jinja',
                'stack_template': { 
                                    'policy_name': project_name + '-service-policy',
                                    'service_instance_name': 'default-domain:' + project_name + ':' + project_name + '-service-instance',
                                    'net_1_name': project_name + '-vnet-1',
                                    'net_2_name': project_name + '-vnet-2'
                                    }
            }
stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack