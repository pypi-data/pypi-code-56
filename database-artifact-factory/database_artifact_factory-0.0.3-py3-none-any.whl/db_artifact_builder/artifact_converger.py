from sceptre.context import SceptreContext
from sceptre.plan.plan import SceptrePlan
import pkg_resources
import os
import yaml
import requests
import subprocess
import time


class ArtifactConverger:
    def __init__(self, create_mode):
        self._create_mode = create_mode

    def converge(self, db_username, db_password, db_name):
        self._patch_client_options(
            db_username, 
            db_password,
            self._my_ip_address()
        )

        project_path = self._sceptre_dir()
        context = SceptreContext(project_path, f"prod/{self._create_mode}.yaml")
        plan = SceptrePlan(context)
        _ = plan.launch()
        endpoint = self._endpoint_from_sceptre_outputs(plan)

        if self._create_mode == 'create':
            self._invoke_liquibase(
                endpoint, 
                db_username, 
                db_password, 
                db_name
            )

        return endpoint

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

    def _invoke_liquibase(self, endpoint, db_username, db_password, db_name):
        subprocess.check_output(
            [
                '/liquibase/liquibase', 
                '--driver=org.postgresql.Driver',
                '--classpath=/liquibase/postgresql-42.2.12.jar',
                f'--url=jdbc:postgresql://{endpoint}:5432/{db_name}',
                '--changeLogFile=/liquibase/changelog.yaml',
                f'--username={db_username}',
                f'--password={db_password}',
                'update'
            ]
        )

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

    def _patch_client_options(self, db_username, db_password, client_ip):
        project_path = self._sceptre_dir()
        config_path = os.path.join(
            project_path, 
            'config', 
            'prod', 
            f"{self._create_mode}.yaml"
        )
        config = self._read_yaml_file(config_path)
        config['parameters']['Username'] = db_username
        config['parameters']['Password'] = db_password
        config['parameters']['ClientIp'] = client_ip
        self._write_yaml_file(
            config,
            config_path
        )



