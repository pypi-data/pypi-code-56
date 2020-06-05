#!/usr/bin/env python
import argparse
import os
import docker
import sys


def converge_artifact_cli():
    arg_parser = argparse.ArgumentParser(description='Converge a database artifact')

    arg_parser.add_argument(
        '--create_mode',            
        type=str,
        choices=['create', 'clone'],
        help='Either create a db from scratch with schema, or clone an existing db',
        required=True
    )
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
        '--db_username',            
        type=str,
        help='The master username for the created db (cloned follows from the source)',
        required=False
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

    if args.create_mode == 'create' and not args.db_username:
        print("If the create_mode is create, the username must be specified")
        sys.exit(1)
    elif args.create_mode == 'create' and args.db_username:
        db_username = args.db_username
    else:
        db_username = 'dontcare'

    client = docker.from_env()
    output = client.containers.run(
        image=args.docker_image,
        volumes={
            args.aws_credentials.name: {'bind': '/root/.aws/credentials', 'mode': 'ro'}
        },
        environment={
            'AWS_PROFILE': args.aws_profile,
            'DB_USERNAME': db_username,
            'DB_PASSWORD': args.db_password,
            'CREATE_MODE': args.create_mode
        }
    )
    print(str(output))

if __name__ == "__main__": 
    converge_artifact_cli()
