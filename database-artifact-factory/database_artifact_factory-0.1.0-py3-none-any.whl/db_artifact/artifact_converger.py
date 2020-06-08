from sceptre.context import SceptreContext
from sceptre.plan.plan import SceptrePlan
import pkg_resources
import os
import yaml
import requests
import subprocess
import time


class ArtifactConverger:
    def __init__(self):
        self._create_mode = 'clone'

    def converge(self, db_password):
        config = self._patch_universal_config()

        self._patch_client_options(
            db_password,
            self._my_ip_address()
        )

        project_path = self._sceptre_dir()
        context = SceptreContext(project_path, f"prod/{self._create_mode}.yaml")
        plan = SceptrePlan(context)
        _ = plan.launch()
        endpoint = self._endpoint_from_sceptre_outputs(plan)

        return endpoint, f"{config['project_code']}-prod-clone"

    ##### PRIVATE ####################

    def _endpoint_from_sceptre_outputs(self, sceptre_plan):
        outputs = list(sceptre_plan.describe_outputs().values())
        output = outputs[0] # only one stack
        stack_outputs = output[f"prod/{self._create_mode}"]
        endpoint_output = filter(
            lambda output: output['OutputKey'] == 'Endpoint',
            stack_outputs
        )
        endpoint = list(endpoint_output)[0]['OutputValue']
        return endpoint

    def _sceptre_dir(self):
        return pkg_resources.resource_filename('db_artifact', 'sceptre')

    def _my_ip_address(self):
        response = requests.get('https://api.ipify.org?format=json')
        return f"{response.json()['ip']}/32"

    def _write_yaml_file(self, config, config_path):
        with open(config_path, 'w') as config_file:
            config_file.write(yaml.dump(config))

    def _read_yaml_file(self, config_path):
        return yaml.load(
            open(config_path, 'r').read(), 
            Loader=yaml.FullLoader
        )

    def _patch_universal_config(self):
        project_path = self._sceptre_dir()
        config_path = os.path.join(
            project_path, 
            'config', 
            'config.yaml'
        )
        config = self._read_yaml_file(config_path)
        config['project_code'] = f"dbartifact{int(time.time())}"
        config['region'] = 'us-east-1'
        self._write_yaml_file(
            config,
            config_path
        )      
        return config

    def _patch_client_options(self, db_password, client_ip):
        project_path = self._sceptre_dir()
        config_path = os.path.join(
            project_path, 
            'config', 
            'prod', 
            f"{self._create_mode}.yaml"
        )
        config = self._read_yaml_file(config_path)
        config['parameters']['Password'] = db_password
        config['parameters']['ClientIp'] = client_ip
        self._write_yaml_file(
            config,
            config_path
        )



