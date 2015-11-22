'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.10.156'
project_name = 'zeppo'

StackData = {   'stack_name': project_name,
                'yaml_file':'../templates/create_project.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'project.jinja',
                'stack_template': { 
                                     'url': config_node_ip,
                                     'description': project_name.upper() + ' Project',
                                     'tenant': project_name,
                                     'enabled': "1",
                                     'user_name': 'admin',
                                     'user_role': 'admin'
                                    }
            }

stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack