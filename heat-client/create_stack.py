'''
Version 2: 
Created on Nov 24, 2017
@author: azaringh + lphan
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


def create_stack( tenant_name='appformix', **kwargs):
    
    #Authenticate
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=auth_url, username=username,password=password,project_name=tenant_name)
    sess = session.Session(auth=auth)
    
    #Heat Client
    heatclient = client.Client('1', session=sess)

    #Open Yaml file, with jinja template
    f = open(kwargs['yaml_file'])
    txt = f.read()
    
    templateLoader = jinja2.FileSystemLoader( searchpath=kwargs['jinja_path'])
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = kwargs['jinja_file']
    template = templateEnv.get_template( TEMPLATE_FILE )
    template_vars = kwargs['stack_template']
    data = yaml.load(template.render( template_vars ))
    
    #Assemble all params
    tx = { "files": {}, "disable_rollback": "true", "stack_name": kwargs['stack_name'], "template": txt, "parameters": data, "environment": {}}
    
    #Create Stack
    stack = heatclient.stacks.create(**tx)
    
    return stack
    
