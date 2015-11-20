'''
Created on Nov 20, 2015

@author: azaringh
'''
import yaml
import jinja2
from heatclient.client import Client as Heat_Client
from keystoneclient.v2_0 import Client as Keystone_Client

config_node_ip = '10.10.10.156'
project_name = 'harpo'

PolicyData =  { 'stack_name': project_name + '-network-policy',
                'policy_template': { 
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

def get_keystone_creds():
    d = {}
    d['username'] = 'admin'
    d['password'] = 'contrail123'
    d['auth_url'] = 'http://' + config_node_ip + ':5000/v2.0'
    d['tenant_name'] = 'admin'
    return d

cred = get_keystone_creds()
ks_client = Keystone_Client(**cred)
heat_endpoint = ks_client.service_catalog.url_for(service_type='orchestration', endpoint_type='publicURL')
heatclient = Heat_Client('1', heat_endpoint, token=ks_client.auth_token)
 
f = open('../templates/network_policy.yaml')
txt = f.read()

templateLoader = jinja2.FileSystemLoader( searchpath="../jinja/")
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "network_policy.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )
templateVars = PolicyData['policy_template']
data = yaml.load(template.render( templateVars ))

tx = { "files": {}, "disable_rollback": "true", "stack_name": PolicyData['stack_name'], "template": txt, "parameters": data, "environment": {}}

stack = heatclient.stacks.create(**tx)
print stack