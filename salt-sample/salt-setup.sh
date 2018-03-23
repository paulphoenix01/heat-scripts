##Download scripts
git clone https://github.com/paulphoenix01/heat-scripts
cd heat-scripts
git checkout auto-scaling



####
sudo add-apt-repository ppa:saltstack/salt
sudo apt-get update
pip install cherrypy==8.1.2
sudo apt-get install -y salt-master salt-api salt-minion salt-ssh salt-cloud salt-doc
mkdir -p /srv/salt/reactor
mkdir -p /srv/salt/pillar
mkdir -p /var/log/salt/event

cd salt-sample
echo -e "2\nNone\nFirstRun\n" > max_instance.log
echo "firewall-service-instance001,0" > /var/log/salt/event/CPU-firewall-service-instance001.log
echo "firewall-service-instance002,0" > /var/log/salt/event/CPU-firewall-service-instance002.log
echo "firewall-service-instance003,0" > /var/log/salt/event/CPU-firewall-service-instance003.log

cp master /etc/salt/master
cp reactor.conf /etc/salt/master.d/.
cp *.sls /srv/salt/reactor/.
echo "master: 192.168.250.4" >> /etc/salt/minion

## already ##
# vim /etc/salt/minion
# master: 192.168.250.4



#vim /usr/lib/python2.7/dist-packages/salt/config.py
'file_ignore_glob': none,
to
'file_ignore_glob': [],

service salt-master restart
service salt-minion restart

#Get the unaccepted keyname
sudo salt-key --list all
sudo salt-call key.finger --local
sudo salt-key -f nugget-linux.juniper.net
sudo salt-key -a nugget-linux.juniper.net

#sudo salt-key -f nugget-appformix.juniper.net
#sudo salt-key -a nugget-appformix.juniper.net

sudo salt-key --list all
sudo salt '*' test.ping

salt-call tls.create_self_signed_cert

# Restart
service salt-master restart
service salt-minion restart



salt-run state.event pretty=True


