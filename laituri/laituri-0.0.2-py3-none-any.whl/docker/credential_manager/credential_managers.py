from .docker_v1 import docker_v1_credential_manager

credential_managers = {
    ('docker', '1'): docker_v1_credential_manager,
}
