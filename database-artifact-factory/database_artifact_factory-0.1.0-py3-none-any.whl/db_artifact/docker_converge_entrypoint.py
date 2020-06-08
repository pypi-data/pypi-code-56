#!/usr/bin/env python
import os
from db_artifact.artifact_converger import ArtifactConverger


mandatory_env_vars = [
    'AWS_PROFILE',
    'DB_PASSWORD'
]
for var in mandatory_env_vars:
    if not os.environ[var]:
        raise Exception(f"Env {var} must be set")

endpoint, stack_name = ArtifactConverger().converge(
    os.environ['DB_PASSWORD']
)
print(f"endpoint: {endpoint}")
print(f"CloudFormation stack; {stack_name}")