import yaml
from ansible.module_utils.basic import AnsibleModule
def role_def(namespace: str, name: str, apigroups: str, resources: str, verbs: str):
    
    verb_mappings = {
        "read": ["get",  "list", "watch"],
        "write": ["get", "list", "watch", "create", "update", "delete"],
        "admin": ["*"]  # Grant all verbs for "admin"
    }
    
    resource_mappings = {
        "low": ["deployments", "pods", "statefulsets", "services", "Events"],
        "medium": ["deployments", "pods", "statefulsets", "services", "Events", "ConfigMaps","Secrets"],
        "high": ["*"]
    }
    apigroups_mapping = {
        "low":["core"],
        "medium":["core","app"],
        "high": [
                "core",
                "apps",
                "batch",
                "networking.k8s.io",
                "storage.k8s.io",
                "rbac.authorization.k8s.io",
                "autoscaling",
                "admissionregistration.k8s.io",
                "policy",
                "scheduling.k8s.io",
                "coordination.k8s.io",
                "flowcontrol.apiserver.k8s.io",
                "certificates.k8s.io",
                "apiextensions.k8s.io",
                "node.k8s.io",
                "authentication.k8s.io",
                "authorization.k8s.io",
                "snapshot.storage.k8s.io"] 
                }
    desired_verbs = verb_mappings.get(verbs)  # Use default empty list for invalid verbs
    desired_resources = resource_mappings.get(resources)  # Use default empty list for invalid resources
    desired_apigroups = apigroups_mapping.get(apigroups)  # Use default empty list for invalid resources

    role_data = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "Role",
        "metadata": {
            "namespace": namespace,
            "name": name
        },
        "rules": [
            {
                "apiGroups": desired_apigroups,
                "resources": desired_resources,
                "verbs": desired_verbs
            }
        ]
    }




    return yaml.dump(role_data, default_flow_style=False)

def main():
    module_args = dict(
        namespace=dict(type='str', required=True),
        name=dict(type='str', required=True),
        apigroups=dict(type='str', required=True),
        resources=dict(type='str', required=True),
        verbs=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False) 


    role_yaml = role_def(
        module.params['namespace'],
        module.params['name'],
        module.params['apigroups'],
        module.params['resources'],
        module.params['verbs']
    )

    # Save the generated YAML to a file (optional)
    with open('/tmp/generated_role.yaml', 'w') as f:
        f.write(role_yaml)

    # Alternatively, return the YAML as a result
    module.exit_json(changed=True, msg="RBAC Role YAML generated successfully", role_yaml=role_yaml)
    print(role_yaml)
#role_def(namespace: str, name: str, apigroups: str, resources: str, verbs: str)
if __name__ == '__main__':
    main()
