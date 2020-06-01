import base64
import configparser
import os
import sys
import traceback

import defusedxml.ElementTree as ET
from os.path import expanduser

import boto.s3
import boto.sts
from aws_access_util.constants import constants
import logging
from datetime import datetime


def saml2AWS(assertion, duration_seconds):
    print(duration_seconds)
    logging.getLogger('boto').setLevel(logging.DEBUG)
    outputformat = constants.outputformat
    awsconfigfile = constants.awsconfigfile
    region = constants.region

    awsroles = []
    root = ET.fromstring(base64.b64decode(assertion))

    for saml2attribute in root.iter(
            '{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        if (saml2attribute.get('Name') ==
                'https://aws.amazon.com/SAML/Attributes/Role'):
            for saml2attributevalue in saml2attribute.iter(
                    '{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                awsroles.append(saml2attributevalue.text)

    # Note the format of the attribute value should be role_arn,principal_arn
    # but lots of blogs list it as principal_arn,role_arn so let's reverse
    # them if needed.
    for awsrole in awsroles:
        chunks = awsrole.split(',')
        if 'saml-provider' in chunks[0]:
            newawsrole = chunks[1] + ',' + chunks[0]
            index = awsroles.index(awsrole)
            awsroles.insert(index, newawsrole)
            awsroles.remove(awsrole)

    # If we have more than one role, ask the user which one they want,
    # otherwise just proceed.
    print("")
    if len(awsroles) > 1:
        i = 0
        print("Please choose the role you would like to assume:")
        for awsrole in awsroles:
            print('[', i, ']: ', awsrole.split(',')[0])
            i += 1

        try:
            print("Selection: ", end=' ')
            selectedroleindex = input()
        except KeyboardInterrupt:
            print('\n')
            print('###################################################################')
            print('# Process Interrupted...exiting out of the program                #')
            print('###################################################################')
            try:
                sys.exit(1)
            except SystemExit:
                os._exit(1)
        except Exception:
            traceback.print_exc(file=sys.stdout)

        # Basic sanity check of input
        if int(selectedroleindex) > (len(awsroles) - 1):
            print('You selected an invalid role index, please try again')
            sys.exit(0)

        role_arn = awsroles[int(selectedroleindex)].split(',')[0]
        principal_arn = awsroles[int(selectedroleindex)].split(',')[1]

    else:
        role_arn = awsroles[0].split(',')[0]
        principal_arn = awsroles[0].split(',')[1]

    # Use the assertion to get an AWS STS token using Assume Role with SAML
    conn = boto.sts.connect_to_region(region)
    try:
        token = conn.assume_role_with_saml(
            role_arn,
            principal_arn,
            assertion,
            duration_seconds=duration_seconds)
    except boto.exception.BotoServerError as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to retrieve aws credentials : {e}'.format(e=e))
        print('###################################################################')
        print('#This may happen if you have specified an out of range duration   #')
        print('###################################################################')
        exit(1)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Connection failure : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)
    # Write the AWS STS token into the AWS credential file
    home = expanduser("~")
    filename = home + awsconfigfile

    # Read in the existing config file
    config = configparser.RawConfigParser()
    config.read(filename)

    # Put the credentials into a saml specific section instead of clobbering
    # the default credentials
    if not config.has_section('saml'):
        config.add_section('saml')

    config.set('saml', 'output', outputformat)
    # config.set('saml', 'region', region)
    config.set('saml', 'aws_access_key_id', token.credentials.access_key)
    config.set('saml', 'aws_secret_access_key', token.credentials.secret_key)
    config.set('saml', 'aws_session_token', token.credentials.session_token)

    # Write the updated config file
    with open(filename, 'w+') as configfile:
        config.write(configfile)

    # Give the user some basic info as to what has just happened
    print('\n\n----------------------------------------------------------------')
    print(
        'Current time in UTC is {cur_date}'.format(
            cur_date=datetime.utcnow()))
    print('Your new access key pair has been stored in the AWS configuration '
          'file {0} under the saml profile.'.format(
              filename))
    print(
        'Note that it will expire at {0}.'.format(
            token.credentials.expiration))
    print('After this time, you may safely rerun this script to refresh '
          'your access key pair.')
    print(
        'To use this credential, call the AWS CLI with the '
        '--profile option (e.g. aws --profile saml ec2 describe-instances).')
    print('----------------------------------------------------------------\n\n')
