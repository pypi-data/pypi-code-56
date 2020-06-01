import boto3

parameter_name = None


def get_value_from_parameter_store(name):
    client = boto3.client('ssm')
    try:
        parameter = client.get_parameter(Name=name, WithDecryption=True)
        return parameter['Parameter']['Value']
    except client.exceptions.ParameterNotFound:
        print("parameter not found")

