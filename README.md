Demo of Auto Scaling with Appformix - Contrail - Heatstack

### Webhook - Event Reactor
- Webhook server listening for alert events on http://192.168.250.4:9999/
- Once an alert event comes from Appformix, the event_reactor reads the alarm and determine if the firewall service need to be scale-out (CPU > 60%), scale-in or do nothing.
    + Service instance scaling is done by updating existing heatclient, which was used to create the firewall service.

## Step-by-step 
### Webhook Setup
Clone this repo and switch to branch autoscaling-webhook
```
git clone https://github.com/paulphoenix01/heat-scripts
cd heat-scripts
git checkout autoscaling-webhook
```

Run heat-client to create 2 VMs - 2 Network topology
```
cd heat-client
python deploy_vm.py create-vm-stack appformix-demo 192.168.1.0/24 192.168.2.0/24
sleep 10
python create_service_template.py fw-template-stack firewall
sleep 5	
python create_service_instance.py fw-instance-stack firewall firewall appformix-vnet-2 appformix-vnet-1
sleep 120
python create_service_policy.py fw-policy-stack firewall-service-instance appformix-vnet-1 appformix-vnet-2
sleep 5
```

Run the webhook server on port 9999
```
cd ../webhook
python webhook.py 9999
```

### AppFormix Setup
(Optional) Change the AppFormix update interval to 10sec
```
curl -X PUT http://192.168.250.3:42595/appformix/v1.0/usage_post_interval?post_interval=10
```

Add new custom notification service endpoint.
```
Left upper corner, select Settings > Notification Settings > Notification Services
Name: webhook
URL endpoint: http://192.168.250.4:9999/

Select "Setup"
```

Setup Alarm (Tab Alarm)
```
Select "Add Rule"
    - Scope: instance. 
    - Project: Appformix
    - Generate Alert
    - Metric: CPU Usage
    - When (within interval): Average value
    - Interval: 20s
    - Threshold: Above 60%
    - Notification: Custom Service
        Select previously created notification service
```

### OpenStack Setup
Using OpenStack GUI, check IP address and perform ping test between VM1 - VM2.

Run iPerf
```
#VM 1 (192.168.1.2): 
iperf -s
```
```
#VM 2 (192.168.2.2):
iperf -c 192.168.1.2 -t 90s
```


### Result
Refer to the powerpoint slides for more details.
![charts](https://i.imgur.com/5o91Ssm.png)

