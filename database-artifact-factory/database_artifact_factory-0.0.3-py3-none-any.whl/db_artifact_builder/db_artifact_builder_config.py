import configparser
import os
import re
from db_artifact_builder.config_exception import ConfigException

class DbArtifactBuilderConfig:
    def parse(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)

        config = configparser.ConfigParser()
        config.read(file_path)

        missing_sections = set(self._mandatory_keys().keys()) - set(config.sections())
        if missing_sections:
            raise ConfigException(f"Missing sections: {missing_sections}")

        for section_name in self._mandatory_keys().keys():
            self._verify_section_keys(section_name, config[section_name])

        if not self._validate_subnet_ids(config):
            raise ConfigException("target_db/subnet_ids must be set to source or a comma-delmited-list of subnets, e.g subnet-1,subnet2,subnet-3")

        #if not self._validate_vpc_id(config):
        #    raise ConfigException("target_db/vpc_id must be set to source or a vpc id, e.g vpc-1234")

        if config['source_db']['liquibase_changelog_path'] != 'dontcare':
            if not os.path.isfile(config['source_db']['liquibase_changelog_path']):
                raise ConfigException("source_db/liquibase_changelog_path must be a local file path")

            if not config['source_db']['liquibase_changelog_path'].endswith('.yaml'):
                raise ConfigException("source_db/liquibase_changelog_path must be a .yaml file")

        return config

    def _validate_vpc_id(self, config):
        vpc_id = config['target_db']['vpc_id']
        if vpc_id == 'source':
            return True
        return re.match('vpc-[0-9a-f]+', vpc_id)

    def _validate_subnet_ids(self, config):
        subnet_ids = config['target_db']['subnet_ids']
        if subnet_ids == 'source':
            return True
        return self._is_comma_delimited_list(subnet_ids)
        
    def _is_comma_delimited_list(self, string):
        cdl_regex = '(subnet-[0-9a-f]+)(,\\s*subnet-[0-9a-f]+)*'
        return re.match(cdl_regex, string)

    def _verify_section_keys(self, section_name, actual_keys):
        missing_keys = set(self._mandatory_keys()[section_name]) - set(actual_keys)
        if missing_keys:
            raise ConfigException(f"Missing {section_name} key: {missing_keys}")

    def _mandatory_keys(self):
        return {
            'source_db': [
                'source_db_cluster_id',
                'liquibase_changelog_path'
            ],
            'target_db': [
                'subnet_ids',
                'instance_type',
                'database_name'
            ]
        }
