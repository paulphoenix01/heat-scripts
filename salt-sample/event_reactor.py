import os
import os.path as path


os.chdir('/root/heat-scripts')
base_path = os.getcwd()
update_py_path = base_path + '/heat-client/update_service_instance.py'
max_instance_path = base_path + '/salt-sample/max_instance.log'

with open("/var/log/salt/event/event.log") as f:
	lines = f.readlines()

with open(max_instance_path) as f:
	instances = f.readlines()


def run_update_script(max_instance, alerted_name):
	cmd = 'python ' + update_py_path + ' fw-instance-stack firewall firewall appformix-vnet-1 appformix-vnet-2 ' + str(max_instance)
	print "Running " + cmd

	list = [ max_instance, alerted_name, cmd ]

	with open(max_instance_path, "w") as f:
		for item in list:
			f.write(str(item) +'\n')
	os.system(cmd)

latest_event = lines[-1].split(" ")

alerted_instance = instances[1].rstrip()
max_instance = int(instances[0])

instance_name = latest_event[1]
metric_value = float(latest_event[-1])

print "Instance " + instance_name + "\t CPU: " + str(metric_value)

#Only check firewall CPU services
if 'firewall' in instance_name:
	print "Alerted: " + alerted_instance + " and instance_name: " + instance_name
	if metric_value >= 60 and max_instance == 2:
		#update - scale up to 3
		run_update_script(3, instance_name)

	elif metric_value < 40 and max_instance == 3 and alerted_instance == instance_name:
		#update - scale down to 2
		msg = "Scaling Down >>> metric: " + str(metric_value) + " max: " + max_instance + "alerted_instance " + alerted_instance
		run_update_script(2, msg)
	else:
		print "CPU: " + str(metric_value) + " and Max_instance: " + str(max_instance) + ", no further action needed"

