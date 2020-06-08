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

    session = boto3.Session()
    image_id = ImageBuilder(args.config_file.name, session).publish()
    print(f"image id: {image_id}")

if __name__ == "__main__": 
    build_artifact_cli()
