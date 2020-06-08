import json

def response_json(data,statusCode):
    return {
        "isBase64Encoded": False,
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "X-Requested-With": '*',
            "Access-Control-Allow-Headers": '*',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": '*'
        },
        "body": json.dumps(data, ensure_ascii=False)
    }