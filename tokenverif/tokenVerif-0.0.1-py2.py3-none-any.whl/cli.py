"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mtokenVerif` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``tokenVerif.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``tokenVerif.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys

import jwt
import cryptography
import boto3
import os
import json


def read_public_key():
    s3client = boto3.client(
        's3',
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name = os.getenv('AWS_DEFAULT_REGION')
    )
     
    # These define the bucket and object to read
    bucketname = 'publickey111'
    file_to_read = 'jwt-key.pub'

    #Create a file object using the bucket and object key. 
    fileobj = s3client.get_object(
        Bucket=bucketname,
        Key=file_to_read
        ) 
    # open the file object and read it into the variable filedata. 
    filedata = fileobj['Body'].read()

    # file data will be a binary stream.  We have to decode it 
    content = filedata.decode('utf-8')
    
    return content



    
def validate_token(j_token):

    j_token_dict = json.loads(j_token)
    token = j_token_dict['token']
    
    
    public_key = read_public_key()
    #print(public_key)
    try:
        decoded_data = jwt.decode(token, key=public_key, algorithms='RS256')
        print('Signature verification successful')
        return decoded_data
    except:
        print('Signature verification failed!')
    

def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """
    data = validate_token(argv)
    #print(argv)
    return data
