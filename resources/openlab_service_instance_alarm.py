from heat.engine import properties
from vnc_api import vnc_api
from contrail_heat.resources.contrail import ContrailResource
import uuid
import logging
import json
from heat.db import api as db_api

logging.basicConfig(filename='LOGexample.log',level=logging.DEBUG)

class ServiceInstanceAlarm(ContrailResource):
    PROPERTIES = (
        NAME, SERVICE_INSTANCE, METER_NAME, THRESHOLD, COMPARISON_OPERATOR, STATISTICS, 
	PERIOD, EVALUATION_PERIODS, ALARM_ACTIONS, OK_ACTIONS, UPDATE_TIMESTAMP,
    ) = (
        'name', 'service_instance', 'meter_name', 'threshold', 'comparison_operator', 'statistics', 
	'period', 'evaluation_periods', 'alarm_actions', 'ok_actions', 'update_timestamp',
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Service instance alarm name'),
            update_allowed=False,
        ),
        SERVICE_INSTANCE: properties.Schema(
            properties.Schema.STRING,
            _('Service instance name'),
            update_allowed=False,
        ),
        METER_NAME: properties.Schema(
            properties.Schema.STRING,
            _('Meter name'),
            update_allowed=False,
        ),
        THRESHOLD: properties.Schema(
            properties.Schema.INTEGER,
            _('Threshold'),
            update_allowed=False,
        ),
        COMPARISON_OPERATOR: properties.Schema(
            properties.Schema.STRING,
            _('Comparison operator'),
            update_allowed=False,
        ),
        STATISTICS: properties.Schema(
            properties.Schema.STRING,
            _('Statistics'),
            update_allowed=False,
        ),
        PERIOD: properties.Schema(
            properties.Schema.INTEGER,
            _('Observation period'),
            update_allowed=False,
        ),
        EVALUATION_PERIODS: properties.Schema(
            properties.Schema.INTEGER,
            _('Number of observation periods'),
            update_allowed=False,
        ),
        ALARM_ACTIONS: properties.Schema(
            properties.Schema.LIST,
            _('List of alarm actions'),
            update_allowed=False,
        ),
        OK_ACTIONS: properties.Schema(
            properties.Schema.LIST,
            _('List of ok actions'),
            update_allowed=False,
        ),
        UPDATE_TIMESTAMP: properties.Schema(
            properties.Schema.STRING,
            _('Update timestamp'),
            update_allowed=True,
        ),
    }

    attributes_schema = {
        "name": _("Comination alarm name."),
        "alarm_ids": _("List of alarms in comination alarm."),
    }

    def handle_create(self):
        db_api.resource_data_set(self, 'name', self.properties[self.NAME], redact=True)
        logging.warning("ServiceInstanceAlarm handle_create called.")
        si_obj = self.vnc_lib().service_instance_read(fq_name_str=self.properties[self.SERVICE_INSTANCE])
        vm_alarms = []
        for vms in si_obj.get_virtual_machine_back_refs() or []:
          vm = self.nova().servers.get(vms['to'][0])
          alarms = self.ceilometer().alarms.create(name =vm.name + '-alarm',meter_name=self.properties[self.METER_NAME], 
                                            threshold=self.properties[self.THRESHOLD],
                                            comparison_operator=self.properties[self.COMPARISON_OPERATOR],
					    statistic=self.properties[self.STATISTICS],
                                            period=self.properties[self.PERIOD],
					    evaluation_periods=self.properties[self.EVALUATION_PERIODS],
                                            alarm_actions=self.properties[self.ALARM_ACTIONS],
                                            ok_actions=self.properties[self.OK_ACTIONS],
                                            matching_metadata={'resource_id': vms['to'][0]})
          vm_alarms.append(alarms.alarm_id.encode())

        vm_alarms = json.dumps(vm_alarms)
        logging.warning("ServiceInstanceAlarm:handle_create vm_alarms: %s.", vm_alarms)
        db_api.resource_data_set(self, 'alarm_ids', vm_alarms, redact=True)
    
        
    def _show_resource(self):
        pass

    def handle_delete(self):
        vm_alarms = json.loads(db_api.resource_data_get(self, 'alarm_ids'))
        logging.warning("ServiceInstanceAlarm:handle_delete vm_alarms: %s.", vm_alarms)
        for a in vm_alarms:
          self.ceilometer().alarms.delete(a)

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
      pass

def _resolve_attribute(self, name):
        if name == 'alarm_ids':
            return db_api.resource_data_get(self, 'alarm_ids')
        elif name == 'name':
            return db_api.resource_data_get(self, 'name')

def resource_mapping():
    return {
        'OS::OpenLab::ServiceInstanceAlarm': ServiceInstanceAlarm
    }
