'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.10.156'
project_name = 'zeppo'

StackData = {   'stack_name': project_name + '-network-policy',
                'yaml_file':'../templates/network_policy.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'network_policy.jinja',
                'stack_template': { 
                                    'policy_name': project_name + '-network-policy',
                                    'direction': '<>',
                                    'action': 'pass',
                                    'start_src_ports': -1,
                                    'end_src_ports': -1,
                                    'start_dst_ports': -1,
                                    'end_dst_ports': -1,
                                    'net_1_name': project_name + '-vnet-1',
                                    'net_2_name': project_name + '-vnet-2'
                                    }
            }

stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack