all:
  vars:
    ansible_ssh_private_key_file: ${key_name}
    ansible_user: ${ssh_user}
    ansible_python_interpreter: /usr/bin/python3
  children:
    monitoring_instances:
      hosts:
%{ for ip in monitoring_instances_ips ~}
%{ if ip == monitoring_instances_ips[0] ~}
        Monithor_Frontend:
          ansible_host: ${ip}
%{ else ~}
        Monithor_Backend:
          ansible_host: ${ip}
%{ endif ~}
%{ endfor ~}