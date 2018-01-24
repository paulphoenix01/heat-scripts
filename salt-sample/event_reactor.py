import os
import os.path as path

#Change working directory
os.chdir('/root/heat-scripts')
base_path = os.getcwd()
update_py_path = base_path + '/heat-client/update_service_instance.py'
max_instance_path = base_path + '/salt-sample/max_instance.log'

#Open event.log file and max_instance.log
with open("/var/log/salt/event/event.log") as f:
	lines = f.readlines()

with open(max_instance_path) as f:
	instances = f.readlines()


#Function for executing heat-client python file
def run_update_script(max_instance, alerted_name):
	cmd = 'python ' + update_py_path + ' fw-instance-stack firewall firewall appformix-vnet-1 appformix-vnet-2 ' + str(max_instance)
	print "Running " + cmd

	list = [ max_instance, alerted_name, cmd ]

	#Update max_instance.log 
	with open(max_instance_path, "w") as f:
		for item in list:
			f.write(str(item) +'\n')
	os.system(cmd)


#Check 3 latest event
#Reason: sometime Appformix send multiple events at once.
latest_events = [lines[-1].split(" "), lines[-2].split(" "), lines[-3].split(" ")]

#Check last scale-out instance
alerted_instance = instances[1].rstrip()
max_instance = int(instances[0])

for latest_event in latest_events:
	instance_name = latest_event[1]		#event instance name
	metric_value = float(latest_event[-1])	#CPU % usage

	#Only check firewall services
	if 'firewall' in instance_name:
		#print "Alerted: " + alerted_instance + " and instance_name: " + instance_name
		#If CPU > 60% and current max_instance=2
		if metric_value >= 60 and max_instance == 2:
			#Scale out 2->3
			run_update_script(3, instance_name)
		
		#If CPU < 40% and current max_instance=3
		elif metric_value < 40 and max_instance == 3 and alerted_instance == instance_name:
			#Scale in 3->2
			run_update_script(2, instance_name)
		else:	#Do nothing
			print "CPU: " + str(metric_value) + " and Max_instance: " + str(max_instance) + ", no further action needed"

