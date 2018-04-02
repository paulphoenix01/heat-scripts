rm -rf /var/log/salt/event/*
echo -e "2\nNone\nFirstRun\n" > max_instance.log
echo -e "2\nNone\nFirstRun\n" > /var/log/salt/event/max_instance.log
echo "firewall-service-instance001,0" > /var/log/salt/event/CPU-firewall-service-instance001.log
echo "firewall-service-instance002,0" > /var/log/salt/event/CPU-firewall-service-instance002.log
echo "firewall-service-instance003,0" > /var/log/salt/event/CPU-firewall-service-instance003.log
