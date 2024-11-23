#!/usr/bin/python
import yaml
from ansible.module_utils.basic import AnsibleModule

# Function to generate a Role based on access level
def generate_role(namespace: str, role_name: str, access_level: str):
    rules = {
        "low": [
            {"apiGroups": [""], "resources": ["pods"], "verbs": ["get", "list"]}
        ],
        "medium": [
            {"apiGroups": [""], "resources": ["pods", "deployments"], "verbs": ["get", "list", "create", "update"]}
        ],
        "high": [
            {"apiGroups": [""], "resources": ["*"], "verbs": ["*"]}
        ],
    }

    if access_level not in rules:
        raise ValueError(f"Invalid access level: {access_level}")

    role = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "Role",
        "metadata": {
            "name": role_name,
            "namespace": namespace
        },
        "rules": rules[access_level]
    }
    return yaml.dump(role, default_flow_style=False)

# Function to generate a ClusterRoleBinding
def generate_cluster_role_binding(binding_name: str, user_name: str, role_name: str):
    cluster_role_binding = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {
            "name": binding_name
        },
        "subjects": [
            {
                "kind": "User",
                "name": user_name,
                "apiGroup": "rbac.authorization.k8s.io"
            }
        ],
        "roleRef": {
            "kind": "ClusterRole",
            "name": role_name,
            "apiGroup": "rbac.authorization.k8s.io"
        }
    }
    return yaml.dump(cluster_role_binding, default_flow_style=False)

# Main function
def main():
    module_args = dict(
        namespace=dict(type='str', required=True),
        binding_name=dict(type='str', required=True),
        user_name=dict(type='str', required=True),
        role_name=dict(type='str', required=True),
        access_level=dict(type='str', required=True, choices=["low", "medium", "high"]),
        generate=dict(type='str', required=True, choices=["role", "clusterrolebinding"])
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False)

    namespace = module.params['namespace']
    binding_name = module.params['binding_name']
    user_name = module.params['user_name']
    role_name = module.params['role_name']
    access_level = module.params['access_level']
    generate = module.params['generate']

    try:
        if generate == "role":
            # Generate Role YAML
            result_yaml = generate_role(namespace, role_name, access_level)
        elif generate == "clusterrolebinding":
            # Generate ClusterRoleBinding YAML
            result_yaml = generate_cluster_role_binding(binding_name, user_name, role_name)
        else:
            module.fail_json(msg="Invalid 'generate' option provided.")

        # Save the YAML to a file
        output_file = f"/tmp/generated_{generate}.yaml"
        with open(output_file, 'w') as f:
            f.write(result_yaml)

        # Return success
        module.exit_json(changed=True, msg=f"{generate.capitalize()} YAML generated successfully.", output_file=output_file)

    except Exception as e:
        module.fail_json(msg=f"Error generating YAML: {str(e)}")

if __name__ == '__main__':
    main()