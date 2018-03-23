import os, sys, json
import os.path as path
from filelock import Timeout, FileLock

#Change working directory
os.chdir('/root/heat-scripts')
base_path = os.getcwd()
update_py_path = base_path + '/heat-client/update_service_instance.py'
max_instance_path = base_path + '/salt-sample/max_instance.log'

user_input = sys.argv
reporting_instance = user_input[1]
log_file =  "CPU-" + reporting_instance + ".log"
log_path = "/var/log/salt/event/" + log_file

# Lock for max_instance.log
lock_path = 'max_instance.log.lock'
lock = FileLock(lock_path, timeout=1)

#Open event.log file and max_instance.log
with open(log_path) as f:
	lines = f.readlines()

try: 
	with lock.acquire(timeout=10):
		with open(max_instance_path, 'r') as f:
			max_instance_log = f.readlines()
except Timeout:
	print "Another process is writing max instance"

#Function for executing heat-client python file
def run_update_script(max_instance, alerted_name):
	cmd = 'python ' + update_py_path + ' fw-instance-stack firewall firewall appformix-vnet-1 appformix-vnet-2 ' + str(max_instance)
	list = []
	if max_instance == 2:
		list = [ str(max_instance), "None", cmd ]
	elif max_instance == 3:
		list = [ str(max_instance), alerted_name, cmd ]

	#Update max_instance.log 
	with open(max_instance_path, "w") as f:
		for item in list:
			f.write(str(item) +'\n')
	os.system(cmd)


#Check last entry
if lines[-1] is not None:
	line = lines[-1].split(",")

instance_name = reporting_instance
cpu_metric = line[1]

#Check max_instance
max_instance = max_instance_log[0]
last_alerted_instance = max_instance_log[1]


if "firewall" in instance_name: 
	if int(cpu_metric) >= 60 and int(max_instance) == 2: 
		#Scale out 2->3
		run_update_script(3, instance_name)
	elif int(cpu_metric) < 40 and int(max_instance) == 3 and instance_name == last_alerted_instance:
		#Scale in 3->2
		run_update_script(2, instance_name)
	else:
		print instance_name + "\tCPU: " + str(cpu_metric).rstrip("\n") + " and Max_instance: " + str(max_instance).rstrip("\n") + ", no further action needed"

lock.release()

#############
'''
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
'''
