#!/usr/bin/env python
import argparse
import boto3
from db_artifact_builder.image_builder import ImageBuilder

def build_artifact_cli():
    arg_parser = argparse.ArgumentParser(description='Publish a database artifact')

    arg_parser.add_argument(
        'config_file',
        type=argparse.FileType('r'),
        help='path to ini file'
    )

    args = arg_parser.parse_args()

    rds_client = boto3.client('rds')
    image_id = ImageBuilder(args.config_file.name, rds_client).publish()
    print(f"image id: {image_id}")

if __name__ == "__main__": 
    build_artifact_cli()
