python create_public_net.py public-net-stack public-net 10.1.102.0/24
sleep 5
python create_vm.py create-vm1-stack demo-vm1 192.168.1.0/24
sleep 5
python create_vm.py create-vm2-stack demo-vm2 192.168.2.0/24
sleep 60
echo "... Waiting for VMs to boot ..."

python attach_net_policy.py attach-policy-stack vm1-vnet vm2-vnet
sleep 5
python attach_net_policy.py attach-policy-stack public-net vm1-vnet
sleep 5
python attach_net_policy.py attach-policy-stack public-net vm2-vnet
sleep 5
