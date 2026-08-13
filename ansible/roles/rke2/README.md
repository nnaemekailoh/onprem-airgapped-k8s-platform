Role Name
=========

Deploy RKE2


Role Variables
--------------

container_registry  
registry_username  
registry_password  
token  
kube_vip_tag  
kube_vip_dns  


Example Playbook
----------------

ansible-playbook -i inventory.py playbooks/deploy-rke2.yml
