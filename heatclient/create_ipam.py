'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.10.156'
project_name = 'zeppo'

StackData = {   'stack_name': project_name + '-ipam',
                'yaml_file':'../templates/ipam.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'ipam.jinja',
                'stack_template': { 
                                     'ipam_name': project_name + '-ipam'
                                    }
            }

stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack