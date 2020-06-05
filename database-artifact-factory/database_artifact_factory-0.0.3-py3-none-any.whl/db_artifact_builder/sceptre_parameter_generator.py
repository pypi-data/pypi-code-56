from db_artifact_builder.network_discovery import NetworkDiscovery
import tempfile
import yaml

class SceptreParameterGenerator:
    def __init__(self, session):
        self._session = session

    def generate(self, config, output_path, create_mode):
        if config['target_db']['subnet_ids'] == 'source':
            source_subnet_ids, source_vpc_id = self._discover_network(config['source_db']['source_db_cluster_id']) 
            subnet_ids = ','.join(source_subnet_ids)
            vpc_id = source_vpc_id
        else:
            subnet_ids_str = config['target_db']['subnet_ids']
            subnet_ids = subnet_ids_str.split(',')
            vpc_id = self._discover_vpc_id(subnet_ids[0]) 

        parameters = {
            'SourceCluster': config['source_db']['source_db_cluster_id'],
            'SubnetIds': subnet_ids,
            'VpcId': vpc_id,
            'DbInstanceClass': config['target_db']['instance_type'],
            'DatabaseName': config['target_db']['database_name']
        }
        sceptre_config = {
            'template_path': f'{create_mode.lower()}.yaml',
            'parameters': parameters
        }
        
        with open(output_path, 'w') as parameter_file:
            parameter_file.write(yaml.dump(sceptre_config))

        return output_path

    def _discover_network(self, db_cluster_id):
        return NetworkDiscovery(self._session).discover_db_subnetgroup_info(db_cluster_id)

    def _discover_vpc_id(self, subnet_id):
        return NetworkDiscovery(self._session).discover_vpc_id(subnet_id)
