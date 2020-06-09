from boto3.dynamodb.types import DYNAMODB_CONTEXT
import decimal

DYNAMODB_CONTEXT.traps[decimal.Inexact] = False
DYNAMODB_CONTEXT.traps[decimal.Rounded] = False


def DynamoEncode(obj):
    if isinstance(obj, dict):
        for key, item in obj.items():
            obj[key] = DynamoEncode(obj[key])
    elif isinstance(obj, list):
        out = []
        for item in obj:
            out.append(DynamoEncode(item))
        obj = out
    elif isinstance(obj, float):
        obj = DYNAMODB_CONTEXT.create_decimal_from_float(obj)
    return obj
