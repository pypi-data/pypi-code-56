import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument('--bucket', '-b', required=True)
parser.add_argument('--prefix', '-pre', required=True)
parser.add_argument('--profile', '-p', default='default')
parser.add_argument('--region', '-r', default='ap-northeast-2')
args = parser.parse_args()

session = boto3.session.Session(profile_name=args.profile)
client = session.client('s3', region_name=args.region)

bucket=args.bucket

def get_objects_list(start_after=''):
    return client.list_objects_v2(
        Bucket=bucket,
        Prefix=args.prefix,
        StartAfter=start_after
    )


def get_acl_params(key):
    response = client.get_object_acl(
        Bucket=bucket,
        Key=key
    )

    return {
        'Owner': response['Owner'],
        'Grants': response['Grants']
    }


def encrypt(key):
    response = client.head_object(
        Bucket=bucket,
        Key=key
    )

    has_already_been_encrypted = 'ServerSideEncryption' in response and response['ServerSideEncryption'] == 'AES256'

    if has_already_been_encrypted:
        print(key + ' has already been encrypted.')

    else:
        acl = get_acl_params(key)

        client.copy_object(
            Bucket=bucket,
            Key=key,
            CopySource={
                'Bucket': bucket,
                'Key': key
            },
            ServerSideEncryption='AES256'
        )

        client.put_object_acl(
            Bucket=bucket,
            Key=key,
            AccessControlPolicy=acl
        )

        print(key + ' has been encrypted.')


def encrypt_bucket():
    object_remains = True
    start_after = ''

    while object_remains:
        objects_list = get_objects_list(start_after)
        objects = objects_list['Contents']

        for object in objects:
            encrypt(object['Key'])

        if len(objects) < 1000:
            object_remains = False
        else:
            start_after = objects[999]['Key']
