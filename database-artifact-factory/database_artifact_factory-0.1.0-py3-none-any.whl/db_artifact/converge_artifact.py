#!/usr/bin/env python
import argparse
import os
import docker
import sys


def converge_artifact_cli():
    arg_parser = argparse.ArgumentParser(description='Converge a database artifact')

    arg_parser.add_argument(
        '--aws_profile',            
        type=str,
        help='the name of the AWS profile to use credentials from',
        default='default'
    )
    arg_parser.add_argument(
        '--aws_credentials',            
        type=argparse.FileType('r'),
        help='the path to the AWS credentials file to mount in the db artifact docker image.  defaults to ~/.aws/credentials',
        default=f"{os.environ['HOME']}/.aws/credentials"
    )
    arg_parser.add_argument(
        '--db_password',            
        type=str,
        help='The master user password for the created db',
        required=True
    )    
    arg_parser.add_argument(
        '--docker_image',            
        type=str,
        default='db-artifact:latest',
        help='The database artifact Docker image name.  defaults to db-artifact:latest'
    )  
    args = arg_parser.parse_args()

    client = docker.from_env()
    output = client.containers.run(
        image=args.docker_image,
        volumes={
            args.aws_credentials.name: {'bind': '/root/.aws/credentials', 'mode': 'ro'}
        },
        environment={
            'AWS_PROFILE': args.aws_profile,
            'DB_PASSWORD': args.db_password
        }
    )
    print(str(output.decode('utf-8')))

if __name__ == "__main__": 
    converge_artifact_cli()
