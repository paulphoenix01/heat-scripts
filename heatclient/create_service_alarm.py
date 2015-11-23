'''
Created on Nov 23, 2015

@author: azaringh
'''
import create_stack
import time, datetime

config_node_ip = '10.10.10.156'
project_name = 'zeppo'

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

StackData = {   'stack_name': project_name + '-service-alarm',
                'yaml_file':'../templates/service_alarm.yaml',
                'jinja_path': '../jinja/',
                'jinja_file': 'service_alarm.jinja',
                'stack_template': { 
                                    'alarm_name': project_name + '-service-alarm',
                                    'instance_name': 'default-domain:' + project_name + ':' + project_name + '-service-instance',
                                    'meter_name': 'cpu_util',
                                    'comparison_operator': 'gt',
                                    'statistics': 'avg',
                                    'threshold': 20,
                                    'period': 60,
                                    'evaluation_periods': 1,
                                    'alarm_actions_url': 'http://controller:8197/alarms/api',
                                    'ok_actions_url': 'http://controller:8197/alarms/api',
                                    'timestamp': timestamp
                                    }
            }
stack = create_stack.create_stack(config_node_ip, project_name, **StackData)
 
print stack