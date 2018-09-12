### How to run

```shell
ansible-playbook -v ./deploy_producer_gcp.yml
```

### Configurations

- credentails/
  Credentail files.
  See [credentails/README.md](credentails/README.md) for more details.

- running_scripts/
  Scripts running in the ansible-playbook.
  See [running_scripts/README.md](running_scripts/README.md) for more details.

- vars/
  Variable files as parameters using in the playbook.

- ansible.cfg
  Default ansible config file.

- deploy_producer_gcp.yml
  Ansible-playbook's yaml file.
