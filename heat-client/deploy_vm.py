'''
Created on Nov 22, 2015

@author: azaringh
'''
import create_stack
import sys
from pprint import pprint

user_input = sys.argv


if len(user_input) != 5 or user_input[2] =='h':
        print "deploy_vm <stack-name> <vm-name> <subnet x.x.x.x/24>"
        print "Example: python deploy_vm.py create-vm-stack appformix-demo 192.168.1.0/24 192.168.2.0/24"
        exit(1)

#Parse User_input
stack_name = user_input[1]
#project_name = user_input[2]
project_name = 'appformix'
vm_name = user_input[2]

net1_prefix = user_input[3]
net1_gw = user_input[3].replace('0/24','254')

net2_prefix = user_input[4]
net2_gw = user_input[4].replace('0/24','254')

StackData_IPAM = {	'stack_name': project_name + '-ipam-sg',
                	'yaml_file':'../templates/ipam.yaml',
                	'jinja_path': '../jinja/',
                	'jinja_file': 'ipam.jinja',
                	'stack_template': { 
                                     'ipam_name': project_name + '-ipam'
                                    }
            	     }
stack = create_stack.create_stack(project_name, **StackData_IPAM)
print "Done deploying IPAM"
pprint(stack)

StackData_VM = [
	      { 'stack_name': stack_name + '-1',                
               'yaml_file':'../templates/deploy_vm.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'deploy_vm.jinja',
                 'stack_template': {
                                         'net_name': project_name + '-vnet-1',
                                         'subnet_name': project_name + '-subnet-1',
                                         'ip_prefix': net1_prefix,
                                         'default_gateway': net1_gw,
                                         'ipam': 'default-domain:' + project_name + ':' + project_name + '-ipam',
                                         'server_name': vm_name + '-vm-1',
                                         'image': 'ubuntu-stress-test',
                                         'flavor': 'm1.medium'
                                         }
                }
               ,
               { 'stack_name': stack_name + '-2',
                'yaml_file':'../templates/deploy_vm.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'deploy_vm.jinja',
                 'stack_template': {
                                         'net_name': project_name + '-vnet-2',
                                         'subnet_name': project_name + '-subnet-2',
                                         'ip_prefix': net2_prefix,
                                         'default_gateway': net2_gw,
                                         'ipam': 'default-domain:' + project_name + ':' + project_name + '-ipam',
                                         'server_name': vm_name + '-vm-2',
                                         'image': 'ubuntu-stress-test',
                                         'flavor': 'm1.medium'
                                         }
                }
               ]

for item in StackData_VM:
    stack = create_stack.create_stack(project_name, **item)
    pprint(stack)

print "Done deploying VMs"
