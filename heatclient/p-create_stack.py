'''
Version 2: 
Created on Nov 24, 2017
@author: azaringh
'''

import yaml
import jinja2
from heatclient import client
from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneauth1 import loading

CONFIG_IP = '192.168.250.1'
username = 'admin'
password = 'contrail123'
auth_url = 'http://' + CONFIG_IP + ':5000/v2.0'
#tenant_name = 'demo'


def get_keystone_session(tenant_name='demo'):
    username = 'admin'
    password = 'contrail123'
    auth_url = 'http://' + CONFIG_IP + ':5000/v2.0'
    tenant_name = tenant_name
    
    auth = v2.Password(username=username, password=password, tenant_name=tenant_name, auth_url=auth_url)

    sess = session.Session(auth=auth)

    return sess

def create_stack( tenant_name='demo', **kwargs):
    
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=auth_url, username=username,password=password,project_name=tenant_name)
    sess = session.Session(auth=auth)

    heatclient = client.Client('1', session=sess)

    print heatclient.stacks.list()
   
    f = open(kwargs['yaml_file'])
    txt = f.read()
    
    templateLoader = jinja2.FileSystemLoader( searchpath=kwargs['jinja_path'])
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = kwargs['jinja_file']
    template = templateEnv.get_template( TEMPLATE_FILE )
    template_vars = kwargs['stack_template']
    data = yaml.load(template.render( template_vars ))
    
    tx = { "files": {}, "disable_rollback": "true", "stack_name": kwargs['stack_name'], "template": txt, "parameters": data, "environment": {}}
    
    stack = heatclient.stacks.create(**tx)
    
    return stack
    
