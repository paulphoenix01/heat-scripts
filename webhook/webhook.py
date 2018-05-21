#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from pprint import pprint
import json, os, sys, time

#Change working directory
os.chdir('..')
base_path = os.getcwd()
update_heat_path = base_path + '/heat-client/update_service_instance.py'

#Basic HTTP Request Handler
class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
    
    #Handle /POST from Appformix    
    def do_POST(self):
        self._set_headers()
        post_data = self.rfile.read(int(self.headers['Content-Length']) ) 
	data = json.loads(post_data)
	#pprint(data)
	        
	handle_alarm(data)


current_max_instance = 2

def handle_alarm(data):
	#pprint(data)
	cpu_value = data['status']['metaData']['Sample_Value']
	alert = data['status']['description']
	instance_name = alert.split(" ")[1]
	
	#print "Alert: %s \nCPU Value: %s \tInstance name: %s" %(alert,cpu_value,instance_name)
	print "Alert: %s" %(alert)
	#Scale Out 2->3
	if cpu_value >= 60 and current_max_instance == 2:
		print "Scaling out from 2->3 firewall service instance.."
		change_max_instance(3)

	elif cpu_value < 60 and current_max_instance == 3:
		print "Scaling in from 3->2 firewall service instance.."
		change_max_instance(2)
	else:
		print "Alarm is processed .. Nothing to do"

	print "--- Current Firewall Instances: %s ---\n" % (str(current_max_instance))
	
def change_max_instance(number):
	global current_max_instance

	#Cmd to run Heatscript for updating service instance
	cmd = 'python ' + update_heat_path + ' fw-instance-stack firewall firewall appformix-vnet-1 appformix-vnet-2 '
	

	if int(number) == 3:
		print "\tRunning heatscript to scale out ..."
		
		current_max_instance = 3		
		cmd += str(3)
		os.system(cmd)

		time.sleep(5)
		print "\t... Done!\n"

	elif int(number) == 2:
		
		print "\tRunning heatscript to scale in ..."
         	current_max_instance = 2       
		cmd += str(2)
                os.system(cmd)
		
		time.sleep(5)
		print "\t... Done!\n"
		
		

## Run HTTP server
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
     

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
