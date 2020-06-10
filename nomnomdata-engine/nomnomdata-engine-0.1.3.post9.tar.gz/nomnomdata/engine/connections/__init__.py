from dataclasses import dataclass

from nomnomdata.engine.components import Connection, Parameter, ParameterGroup
from nomnomdata.engine.parameters import Int, String


@dataclass
class AWSTokenConnection(Connection):
    parameter_groups = {
        "Auth": ParameterGroup(
            Parameter(type=String(), name="token", required=True),
            Parameter(type=Int(), name="number", required=True),
            name="auth",
            description="Auth parameters",
        )
    }
    connection_type_uuid: str = "AWS5D-TO99M"


@dataclass
class FTPConnection(Connection):
    parameter_groups = {
        "Auth": ParameterGroup(
            Parameter(type=String(), name="hostname"),
            name="auth",
            description="Auth parameters",
        )
    }
    connection_type_uuid: str = "FTP92-TS0BZ"
