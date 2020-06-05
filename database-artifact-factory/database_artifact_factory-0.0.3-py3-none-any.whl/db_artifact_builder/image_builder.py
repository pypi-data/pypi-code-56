from db_artifact_builder.db_artifact_builder_config import DbArtifactBuilderConfig
from db_artifact_builder.sceptre_parameter_generator import SceptreParameterGenerator
from shutil import copyfile, copytree, rmtree
import docker
import pkg_resources
import os

class ImageBuilder:
    def __init__(self, config_file, session):
        self._config_file = config_file
        self._session = session

    def publish(self, docker_dir='/var/tmp/db_artifact_builder/'):
        config = DbArtifactBuilderConfig().parse(self._config_file)

        if os.path.exists(docker_dir):
            rmtree(docker_dir)
        os.mkdir(docker_dir)

        output_path = os.path.join(docker_dir, 'sceptre_config_create.yml')
        _ = SceptreParameterGenerator(self._session).generate(config, output_path, 'create')

        output_path = os.path.join(docker_dir, 'sceptre_config_clone.yml')
        _ = SceptreParameterGenerator(self._session).generate(config, output_path, 'clone')

        self._copy_resources_under_docker_dir(
            docker_dir,
            config
        )

        image, output = self._build_image(
            docker_dir,
            config['target_db']['database_name']
        )
        for output_dict in output:
            self._parse_docker_line(output_dict)

        return image.id

    ##################################PRIVATE#################################

    def _write_empty_file(self, path):
        with open(path,'w') as out:
            out.write('')

    def _copy_resources_under_docker_dir(self, docker_dir, config):
        copyfile(
            self._resource('Dockerfile'),
            os.path.join(docker_dir, 'Dockerfile')
        )
        if config['source_db']['liquibase_changelog_path'] != 'dontcare':
            copyfile(
                config['source_db']['liquibase_changelog_path'], 
                os.path.join(docker_dir, 'changelog.yaml')
            )
        else:
            self._write_empty_file(
                os.path.join(docker_dir, 'changelog.yaml')
            )

        copyfile(
            self._config_file, 
            os.path.join(docker_dir, 'published.ini')
        )
        copytree(
            pkg_resources.resource_filename('db_artifact', '/'), 
            os.path.join(docker_dir, 'db_artifact/')
        )

    def _resource(self, resource_name):
        return  pkg_resources.resource_filename('db_artifact_builder', resource_name)

    def _parse_docker_line(self, line_dict):
        try:
            if 'errorDetail' in line_dict:
                raise Exception(line_dict['errorDetail'])
            elif 'stream' in line_dict:
                print(line_dict['stream'])
            else:
                print(line_dict)
        except ValueError:
            pass

    def _build_image(self, docker_dir, db_target_name):
        client = docker.from_env()
        return client.images.build(
            path=docker_dir,
            tag='db-artifact',
            buildargs={
                'DB_TARGET_NAME':db_target_name
            }
        )


