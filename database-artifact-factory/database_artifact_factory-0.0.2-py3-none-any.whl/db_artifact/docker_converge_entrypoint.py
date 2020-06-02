#!/usr/bin/env python
import argparse
import os
from db_artifact.artifact_converger import ArtifactConverger


arg_parser = argparse.ArgumentParser(description='Converge a database artifact')

arg_parser.add_argument('create_mode',
                       type=str,
                       help='create|clone')

args = arg_parser.parse_args()

mandatory_env_vars = [
    'AWS_PROFILE',
    'DB_USERNAME',
    'DB_PASSWORD'
]
for var in mandatory_env_vars:
    if not os.environ[var]:
        raise Exception(f"Env {var} must be set")

target_db_name = open('/DB_TARGET_NAME', 'r').read().strip()

endpoint = ArtifactConverger(create_mode=args.create_mode).converge(
    os.environ['DB_USERNAME'],
    os.environ['DB_PASSWORD'],
    target_db_name
)
print(f"endpoint: {endpoint}")