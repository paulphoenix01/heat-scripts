Demo of Auto Scaling with Appformix - Saltstack - Heatstack

### Salt Event Reactor
- Salt-api listening for alert events on https://192.168.250.4:8000/hook/my/event
- Once an alert event comes from Appformix, reactor will do:
    + Log the event into /var/log/salt/event.log
    + Execute event_reactor.py script.
- The event_reactor reads the log file, and determine if the firewall service need to be scale-out (CPU > 60%), scale-in (CPU < 40%), or does nothing.
    + Scale-in/out is done by updating existing heatclient, which was used to create the firewall service.


### Result
![charts](https://i.imgur.com/5o91Ssm.png)

