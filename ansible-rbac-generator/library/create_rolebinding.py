#!/usr/bin/python
import yaml
from ansible.module_utils.basic import AnsibleModule
def generate_role_binding(namespace: str, binding_name: str, user_name: str, role_name: str):
    role_binding = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
        "metadata": {
            "name": binding_name,
            "namespace": namespace
        },
        "subjects": [
            {
                "kind": "User",
                "name": user_name,
                "apiGroup": "rbac.authorization.k8s.io"
            }
        ],
        "roleRef": {
            "kind": "Role",
            "name": role_name,
            "apiGroup": "rbac.authorization.k8s.io"
        }
    }
    return yaml.dump(role_binding, default_flow_style=False)

def main():
    module_args = dict(
        namespace=dict(type='str', required=True),
        binding_name=dict(type='str', required=True),
        user_name=dict(type='str', required=True),
        role_name=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False) 

    role_binding_yaml = generate_role_binding(
        module.params['namespace'],
        module.params['binding_name'],
        module.params['user_name'],
        module.params['role_name']
    )

    # Save the generated YAML to a file (optional)
    with open('/tmp/generated_rolebinding.yaml', 'w') as f:
        f.write(role_binding_yaml)

    # Return the YAML as a result
    module.exit_json(changed=True, msg="RoleBinding YAML generated successfully", role_binding_yaml=role_binding_yaml)

if __name__ == '__main__':
    main()

