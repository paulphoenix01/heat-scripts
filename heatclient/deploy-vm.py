'''
Created on Nov 19, 2015

@author: azaringh
'''
import time
import yaml
import jinja2
from heatclient.client import Client as Heat_Client
from keystoneclient.v2_0 import Client as Keystone_Client

config_node_ip = '10.10.10.156'
project_name = 'harpo'

DeploymentData = [{ 'stack_name': project_name + '-vnet-1',
                 'deployment_template': {
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
                 'deployment_template': {
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

def get_keystone_creds():
    d = {}
    d['username'] = 'admin'
    d['password'] = 'contrail123'
    d['auth_url'] = 'http://' + config_node_ip + ':5000/v2.0'
    d['tenant_name'] = project_name 
    return d

cred = get_keystone_creds()
ks_client = Keystone_Client(**cred)
heat_endpoint = ks_client.service_catalog.url_for(service_type='orchestration', endpoint_type='publicURL')
heatclient = Heat_Client('1', heat_endpoint, token=ks_client.auth_token)
 
f = open('../templates/deploy_vm.yaml')
txt = f.read()

templateLoader = jinja2.FileSystemLoader( searchpath="../jinja/")
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "deploy_vm.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )

for item in DeploymentData:
    templateVars = item['deployment_template']
    data = yaml.load(template.render( templateVars ))
    tx = { "files": {}, "disable_rollback": "true", "stack_name": item['stack_name'], "template": txt, "parameters": data, "environment": {}}
    stack = heatclient.stacks.create(**tx)
    print stack
    time.sleep(2)
