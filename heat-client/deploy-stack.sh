python create_public_net.py public-net-stack public-net 10.1.102.0/24
sleep 5
python create_vm.py create-vm1-stack demo-vm1 192.168.1.0/24
sleep 5
python create_vm.py create-vm2-stack demo-vm2 192.168.2.0/24
echo "... Waiting 60s for VMs to boot ..."
sleep 60

python attach_network_policy.py attach-policy-stack demo-vm1-vnet demo-vm2-vnet
sleep 5
python attach_network_policy.py attach-policy-stack1 public-net demo-vm1-vnet
sleep 5
python attach_network_policy.py attach-policy-stack2 public-net demo-vm2-vnet
sleep 5
echo "Done"
