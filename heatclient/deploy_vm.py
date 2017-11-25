'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack

config_node_ip = '10.10.13.103'
project_name = 'chico'

StackData = [{ 'stack_name': project_name + '-vnet-1',                
               'yaml_file':'../templates/deploy_vm.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'deploy_vm.jinja',
                 'stack_template': {
                                         'net_name': project_name + '-vnet-1',
                                         'subnet_name': project_name + '-subnet-1',
                                         'ip_prefix': '192.168.1.0/24',
                                         'default_gateway': '192.168.1.254',
                                         'ipam': 'default-domain:' + project_name + ':' + project_name + '-ipam',
                                         'server_name': project_name + '-vm-1',
                                         'image': 'vm-iperf',
                                         'flavor': 'm1.small'
                                         }
                }
               ,
               { 'stack_name': project_name + '-vnet-2',
                'yaml_file':'../templates/deploy_vm.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'deploy_vm.jinja',
                 'stack_template': {
                                         'net_name': project_name + '-vnet-2',
                                         'subnet_name': project_name + '-subnet-2',
                                         'ip_prefix': '192.168.2.0/24',
                                         'default_gateway': '192.168.2.254',
                                         'ipam': 'default-domain:' + project_name + ':' + project_name + '-ipam',
                                         'server_name': project_name + '-vm-2',
                                         'image': 'vm-iperf',
                                         'flavor': 'm1.small'
                                         }
                }
               ]

for item in StackData:
    stack = create_stack.create_stack(config_node_ip, project_name, **item)
    print stack