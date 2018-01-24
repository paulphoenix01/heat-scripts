import os
import os.path as path

#base_path = path.abspath(path.join(os.getcwd(),".."))
os.chdir('/root/heat-scripts')
update_py_path = os.getcwd() + '/heat-client/update_service_instance.py'

with open("/var/log/salt/event/event.log") as f:
	lines = f.readlines()


def run_update_script(instance):
	cmd = 'python ' + update_py_path + ' fw-instance-stack firewall firewall appformix-vnet-1 appformix-vnet-2 ' + str(instance)
	print "Running " + cmd
	os.system(cmd)

latest_event = lines[-1].split(" ")

instance_name = latest_event[1]
metric_value = float(latest_event[-1])

print "Instance " + instance_name + "\t CPU: " + str(metric_value)

#Only check firewall CPU services
if 'firewall' in instance_name:
	if metric_value >= 60:
		#update - scale up to 3
		run_update_script(3)

	elif metric_value < 40:
		#update - scale down to 2 
		run_update_script(2)
