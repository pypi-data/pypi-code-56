import boto3

class NetworkDiscovery:

  def __init__(self, session):
      self._rds_client = session.client('rds')
      self._ec2_client = session.client('ec2')

  def discover_vpc_id(self, subnet_id):
      describe_subnets_response = self._ec2_client.describe_subnets(
          SubnetIds=[
              subnet_id
          ]
      )
      return describe_subnets_response['Subnets'][0]['VpcId']

  def discover_db_subnetgroup_info(self, source_db_cluster):
      '''
      Given an rds aurora db instance id
      When the instance exits 
      And it is running
      And this function is called
      Then the subnet and vpc info is returned in a tuple
      '''

      subnet_group_name = self._rds_client.describe_db_clusters(
          DBClusterIdentifier=source_db_cluster,
      )['DBClusters'][0]['DBSubnetGroup']

      subnet_group = self._rds_client.describe_db_subnet_groups(
        DBSubnetGroupName=subnet_group_name,
      )['DBSubnetGroups'][0]

      subnet_ids = [subnet['SubnetIdentifier'] for subnet in subnet_group['Subnets']]
      vpc_id = subnet_group['VpcId']

      return (subnet_ids, vpc_id) 

if __name__ == '__main__':
    discovery = NetworkDiscovery(boto3.client('rds', region_name='us-east-1'))
    print(discovery.discover_db_subnetgroup_info(source_db_cluster='database-factory-prototype-source-cluster-1d646445oi7to'))
