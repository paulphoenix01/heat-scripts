python create_vm.py create-vm1-stack demo-vm1 192.168.1.0/24
sleep 5
python create_vm.py create-vm2-stack demo-vm2 192.168.2.0/24
echo "... Waiting 60s for VMs to boot ..."
sleep 60

python attach_network_policy.py attach-policy-stack demo-vm1-vnet demo-vm2-vnet
sleep 5

#echo ">> Creating Service template.."
#python create_service_template.py fw-template-stack firewall

#echo "         .. Service Instance .. Net1 <> Firewall <> Net2"
#python create_service_instance.py fw-instance-stack firewall firewall demo-vm1-vnet demo-vm2-vnet

#echo "         .. Service Policy"
#python create_service_policy.py fw-policy-stack firewall-service-instance demo-vm1-vnet demo-vm2-vnet

echo "Done"
