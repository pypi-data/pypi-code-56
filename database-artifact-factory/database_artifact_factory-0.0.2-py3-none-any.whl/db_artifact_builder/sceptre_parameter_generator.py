from db_artifact_builder.network_discovery import NetworkDiscovery
import tempfile
import yaml

class SceptreParameterGenerator:
    def __init__(self, rds_client):
        self._rds_client = rds_client

    def generate(self, config, output_path, create_mode):
        if config['target_db']['subnet_ids'] == 'source' or config['target_db']['vpc_id'] == 'source':
            subnet_ids, vpc_id = self._discover_network(config['source_db']['source_db_cluster_id']) 
            subnet_ids = ','.join(subnet_ids)
        
        if config['target_db']['subnet_ids'] != 'source':
            subnet_ids = config['target_db']['subnet_ids']

        if config['target_db']['vpc_id'] != 'source':
            vpc_id = config['target_db']['vpc_id']

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
        return NetworkDiscovery(self._rds_client).discover_db_subnetgroup_info(db_cluster_id)

