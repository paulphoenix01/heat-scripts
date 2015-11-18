#!/usr/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import subprocess
import os
import time
from ceilometerclient import client

from heatclient.client import Client as Heat_Client
import keystoneclient.v2_0.client as ksclient

def get_keystone_creds(t):
    d = {}
    d['username'] = 'admin'
    d['password'] = 'contrail123'
    d['auth_url'] = 'http://controller:5000/v2.0'
    d['tenant_name'] = t
    return d

ceilometer_client = client._get_ksclient(**get_keystone_creds('admin'))
token = ceilometer_client.auth_token
ceilo_endpoint = 'http://controller:8777'
ceilometer = client.Client('2',endpoint = ceilo_endpoint, token = lambda: token)

app = Flask(__name__)

@app.route('/alarms/api', methods=['POST'])
def create_alarm():
    if not request.json:
        abort(400)
    ks_client = ksclient.Client(**get_keystone_creds('admin'))
    the_alarm = ceilometer.alarms.get(request.json['alarm_id'])
    project_id = the_alarm.project_id
    project_name = ks_client.tenants.get(project_id).name
    instance_stack_name = project_name + '-service-instance'

    ks_client = ksclient.Client(**get_keystone_creds(project_name))
    heat_endpoint = ks_client.service_catalog.url_for(service_type='orchestration', endpoint_type='publicURL')
    heatclient = Heat_Client('1', heat_endpoint, token=ks_client.auth_token)
    instance_stack = heatclient.stacks.get(instance_stack_name)
    max_instances = int(instance_stack.parameters['max_instances'])
    net_one = instance_stack.parameters['net_1_name'].rsplit(':', 3)[2]
    net_two = instance_stack.parameters['net_2_name'].rsplit(':', 3)[2]

    alarm_stack_name = project_name + '-service-alarm'
    alarm_stack = heatclient.stacks.get(alarm_stack_name)

    if( (request.json['current'] == 'alarm') and  (request.json['previous'] == 'ok') ):
        subprocess.call([os.environ['ROOT_DIR']+'/bin/update-service-instance', project_name, net_one, net_two, str(max_instances+1)])

        print request.json['current'], request.json['previous'], request.json['alarm_id'], 'alarm raised: scale-out '+ str(max_instances) + '->' + str(max_instances+1) + ' instances'
        return jsonify({'task': u'Ceilometer alarm raised - scale-out 2 -> 3 instances'}), 201
    elif( (request.json['current'] == 'ok') and  (request.json['previous'] == 'alarm') ):
        subprocess.call([os.environ['ROOT_DIR']+'/bin/update-service-instance', project_name, net_one, net_two, str(max_instances-1)])

        print request.json['current'], request.json['previous'], request.json['alarm_id'], 'alarm cleared: scale-in ' + str(max_instances) + '->' + str(max_instances-1) + ' instances'
        return jsonify({'task': u'Ceilometer alarm cleared - scale-in 3 -> 2 instances'}), 201
    else:
        print 'Unknown state transition'
    return jsonify({'task': u'Ceilometer alarm event received'}), 201

if __name__ == '__main__':
    app.run(host="controller", port=int(os.environ['PORTAL_PORT']), debug=True)

