Demo of using Heat scripts for automating VM and Network creation with Contrail / OpenStack Mitaka

### Running full Heat-stack scripts
Clone the repo
```
git clone https://github.com/paulphoenix01/heat-scripts
```
Go to heat-client, give deploy-stack.sh execute permission, and execute
```
cd heat-scripts/heat-client
chmod 700 deploy-stack.sh
./deploy-stack.sh
```
Output would be as follow
```
root@nugget-linux:~/heat-scripts/heat-client# ./deploy-stack.sh
>>> Creating Stack for Network: public-net
>>> Creating Stack for Spawning VM:  demo-vm1
>>> Creating Stack for Spawning VM:  demo-vm2
... Waiting 60s for VMs to boot ...
>>> Creating Stack for Attaching Network Policy: demo-vm1-vnet<->demo-vm2-vnet
>>> Creating Stack for Attaching Network Policy: public-net<->demo-vm1-vnet
>>> Creating Stack for Attaching Network Policy: public-net<->demo-vm2-vnet
Done
```

### Heat-client explanation
***create_public_net.py***
```
python create_public_net.py <stack-name> <net-name> <subnet 10.1.<dc_number>.x/24>
*** Example: python create_public_net.py public-net-stack public-net 10.1.102.0/24 ***
```

***create_vm.py***

Repeat for vm1 and vm2
```
python create_vm <stack-name> <vm-name> <subnet x.x.x.x/24> 
*** Example: python create_vm.py create-vm1-stack demo-vm1 192.168.1.0/24 ***
```

***attach_network_policy.py***

Policy will allow all TCP/UDP/ICMP between 2 networks

Repeat for vm1-net <> vm2-net, vm1-net <> public-net, vm2-net <> public-net
```
python attach_network_policy <stack-name> <net_1_name> <net_2_name>
*** Example: python attach_network_policy.py attach-policy-stack vm1-vnet vm2-vnet ***
```


### Result
Contrail Network

Public network shows: External = Enabled
![network](https://i.imgur.com/Kx34wBh.png)

Policies
![policies](https://i.imgur.com/GF1EVOe.png)

VMs connectivity
![vms](https://i.imgur.com/nTbd2QY.png)
