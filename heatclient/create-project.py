'''
Created on Nov 19, 2015

@author: azaringh
'''
import yaml
import jinja2
from heatclient.client import Client as Heat_Client
from keystoneclient.v2_0 import Client as Keystone_Client

config_node_ip = '10.10.10.156'
project_name = 'harpo'

ProjectData = { 'stack_name': project_name,
                'project_template': { 
                                     'url': config_node_ip,
                                     'description': project_name.upper() + ' Project',
                                     'tenant': project_name,
                                     'enabled': "1",
                                     'user_name': 'admin',
                                     'user_role': 'admin'
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
 
f = open('../templates/create_project.yaml')
txt = f.read()

templateLoader = jinja2.FileSystemLoader( searchpath="../jinja/")
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "project.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )
templateVars = ProjectData['project_template']
data = yaml.load(template.render( templateVars ))

tx = { "files": {}, "disable_rollback": "true", "stack_name": ProjectData['stack_name'], "template": txt, "parameters": data, "environment": {}}

stack = heatclient.stacks.create(**tx)
print stack