import yaml
from ansible.module_utils.basic import AnsibleModule

def serviceaccount_def(namespace: str, name: str):
    """
    Generate YAML for a Kubernetes ServiceAccount.
    """
    serviceaccount_data = {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {
            "namespace": namespace,
            "name": name
        }
    }
    return yaml.dump(serviceaccount_data, default_flow_style=False)

def main():
    module_args = dict(
        namespace=dict(type='str', required=True),
        serviceaccount_name=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False)

    # Generate ServiceAccount YAML
    serviceaccount_yaml = serviceaccount_def(
        module.params['namespace'],
        module.params['serviceaccount_name']
    )

    # Write the generated YAML to a file
    with open('/tmp/serviceaccount.yaml', 'w') as f:
        f.write(serviceaccount_yaml)

    module.exit_json(changed=True, msg="ServiceAccount YAML generated successfully", serviceaccount_yaml=serviceaccount_yaml)

if __name__ == '__main__':
    main()
