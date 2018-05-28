python deploy_vm.py create-vm-stack appformix-demo 192.168.1.0/24 192.168.2.0/24
sleep 10
python create_service_template.py fw-template-stack firewall
sleep 5	
python create_service_instance.py fw-instance-stack firewall firewall appformix-vnet-2 appformix-vnet-1
echo "Created VMs and Firewall Service Instances... Waiting 120s for VMs to boot ..."
sleep 120

python create_service_policy.py fw-policy-stack firewall-service-instance appformix-vnet-1 appformix-vnet-2
sleep 5
echo "Done"
