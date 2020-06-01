# Note: Requires Python 3.3 or higher

# This module integrates with DUO MFA and generates a
# temporary access and token which are copied
# in the aws credentials file under ./aws. These
# credentials are then used to interact with AWS resources
import os.path
import getpass
import ast
import argparse
import time
import traceback
from os import path
from os.path import expanduser
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('..')
from aws_access_util.constants import constants # noqa: E402
from aws_access_util.constants.constants import call_back_url  # noqa: E402
from aws_access_util.constants.constants import awsconfigfile, \
    awsfolder  # noqa: E402
from jinja2 import Environment, FileSystemLoader, \
    BaseLoader  # noqa: E402
from aws_access_util.common.duo_utilities import get_payload, get_action_url, \
    get_duo_attributes, get_duo_sid, get_assertion  # noqa: E402
from aws_access_util.common.aws_utilities import saml2AWS  # noqa: E402
from aws_access_util.constants.constants import auth_url  # noqa: E402
from aws_access_util.constants.constants import prompt_url  # noqa: E402
from aws_access_util.constants.constants import status_url  # noqa: E402
from aws_access_util.constants.constants import result_url  # noqa: E402


def get_saml_assertion(url, user, password):
    """
    This function integrates with DUO mfa and returns the saml assertion
    :url : The URL of the AWS account
    :user: The userid to connect to the URL
    :password: The password to connect to AWS
    :return: saml assertion
    """
    cisco_url = url.split('/idp')[0]
    session = requests.Session()

    try:
        idp_url_response = session.get(url)

    except requests.exceptions.InvalidSchema as e:
        track = traceback.format_exc()
        print(track)
        print('Connection failure : {e}'.format(e=e))
        print('###################################################################')
        print('#This may happen if the URL is missing https:// at the start      #')
        print('###################################################################')
        exit(1)
    except requests.exceptions.MissingSchema as e:
        track = traceback.format_exc()
        print(track)
        print('Connection failure : {e}'.format(e=e))
        print('###################################################################')
        print('#This may happen if the URL provided is incorrect                 #')
        print('###################################################################')
        exit(1)
    except requests.exceptions.ConnectionError as e:
        track = traceback.format_exc()
        print(track)
        print('Connection failure : {e}'.format(e=e))
        print('###################################################################')
        print('#This may happen if the URL provided is incorrect or not reachable#')
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

    idp_url_response_text = idp_url_response.text

    idp_url_response_soup = BeautifulSoup(
        idp_url_response_text, features="html.parser")
    payload = get_payload(idp_url_response_soup, user, password)
    del user
    del password

    action_url = get_action_url(idp_url_response_soup)

    # Invoke the action URL through a POST call.
    # This will return the duoinit which will need to be
    # parsed to get the duo host name, duo signatures
    # and the post action url
    try:
        response = session.post(
            action_url,
            data=payload,
            verify=constants.sslverification)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get duoinit, error : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)
    response_text = response.text

    response_form_soup = BeautifulSoup(response_text, features="html.parser")
    # IF MFA is not required for generic accounts just return from here with
    # the assertion
    for inputtag in response_form_soup.find_all('input'):
        if (inputtag.get('name') == 'SAMLResponse'):
            # print(inputtag.get('value'))
            saml_assertion = inputtag.get('value')
            return saml_assertion

        else:
            break

    try:
        duo_host, duo_signatures, duo_callback = get_duo_attributes(
            response_form_soup)
    except IndexError as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get duo attribute, error : {e}'.format(e=e))
        print('###################################################################')
        print('# This may happen if you have not provided the right credentials  #')
        print('###################################################################')
        exit(1)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get duo attribute, error : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)

    # Now call the auth URL to get the SID
    auth_url_formatted = auth_url.format(
        duo_host=duo_host) + "?tx=" + duo_signatures[0] \
        + "&parent=https://cloudsso.cisco.com/" \
        + duo_callback + "?&v=2.6"

    try:
        auth_response = session.post(auth_url_formatted)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get response from auth url : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)

    auth_response_text = auth_response.text
    auth_response_form_soup = BeautifulSoup(
        auth_response_text, features="html.parser")
    duo_sid = get_duo_sid(auth_response_form_soup)
    prompt_url_formatted = prompt_url.format(duo_host=duo_host)

    # Prompts the user to enter the DUO authentication mechanism
    i = 0
    options = constants.options
    print("Choose an authentication method:")
    for option in options:
        print('[', i, ']: ', option.split(',')[0])
        i += 1
    try:
        print("Selection: ", end=' ')
        selectedauthenticationmethod = input()
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

    factor = options[int(selectedauthenticationmethod)].split(',')[1]
    passcode = ''
    if (factor == 'sms' or factor == 'Passcode'):
        if(factor == 'sms'):
            prompt_url_formatted = prompt_url_formatted + "?sid=" + \
                duo_sid + "&device=phone1&factor=" + factor
            try:
                prompt_url_response = session.post(prompt_url_formatted)
                factor = 'Passcode'
            except Exception as e:
                track = traceback.format_exc()
                print(track)
                print('Failed to get response from sms : {e}'.format(e=e))
                print(
                    '###################################################################')
                print(
                    '# Please connect with the support team and share the error message#')
                print(
                    '###################################################################')
                exit(1)

        print("Enter Passcode: ", end=' ')
        try:
            passcode = input()
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
        prompt_url_formatted = prompt_url_formatted + "?sid=" + duo_sid + \
            "&device=phone1&factor=" + factor + "&passcode=" + passcode
    else:
        prompt_url_formatted = prompt_url_formatted + "?sid=" + \
            duo_sid + "&device=phone1&factor=" + factor
    try:
        prompt_url_response = session.post(prompt_url_formatted)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get response : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)

    prompt_url_response_text = prompt_url_response.text
    prompt_url_response_json = ast.literal_eval(prompt_url_response_text)
    duo_tx_stat = prompt_url_response_json["stat"]
    duo_tx_id = prompt_url_response_json["response"]["txid"]
    if duo_tx_stat != 'OK':
        print("Invalid response from duo mfa device")
        raise Exception

    # get the status of prompt
    status_url_formatted = status_url.format(duo_host=duo_host)
    status_url_formatted = status_url_formatted + \
        "?sid=" + duo_sid + "&txid=" + duo_tx_id
    while True:
        try:
            status_url_response = session.post(status_url_formatted)
        except Exception as e:
            track = traceback.format_exc()
            print(track)
            print('Failed to get response: {e}'.format(e=e))
            print('###################################################################')
            print('# Please connect with the support team and share the error message#')
            print('###################################################################')
            exit(1)

        status_url_response_text = status_url_response.text
        status_url_response_json = ast.literal_eval(status_url_response_text)

        try:
            duo_tx_result = status_url_response_json['response']['result']
            duo_tx_status = status_url_response_json['response']['status']
            duo_tx_status_code = \
                status_url_response_json['response']['status_code']
        except KeyError:
            duo_tx_result = ''

        try:
            duo_result_url = status_url_response_json['response']['result_url']
        except KeyError:
            duo_result_url = ''

        try:
            if duo_tx_result == 'FAILURE':
                raise Exception
        except Exception:
            print(duo_tx_status_code + "::" + duo_tx_status)
            exit(1)

        if duo_tx_result == 'SUCCESS':
            break
        else:
            time.sleep(0.2)

    # Get the cookie
    result_url_formatted = result_url.format(
        duo_host=duo_host, duo_result_url=duo_result_url)
    result_url_formatted = result_url_formatted + \
        "?sid=" + duo_sid + "&txid=" + duo_tx_id

    try:
        result_url_response = session.post(result_url_formatted)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get response : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)

    result_url_response_text = result_url_response.text
    result_url_response_json = ast.literal_eval(result_url_response_text)
    sig_response = result_url_response_json['response']['cookie'] + \
        ":" + duo_signatures[1]

    # Call back parent URL with ths sig_response
    call_back_url_formatted = call_back_url.format(
        cisco_url=cisco_url,
        duo_callback=duo_callback,
        sig_response=sig_response)
    try:
        call_back_url_response = session.post(call_back_url_formatted)
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Failed to get response : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)
    call_back_url_response_text = call_back_url_response.text
    call_back_url_response_soup = BeautifulSoup(
        call_back_url_response_text, features="html.parser")
    saml_assertion = get_assertion(call_back_url_response_soup)

    return saml_assertion


def create_default_profile():
    """
    This function creates the default profile
    under .aws folder, if the profile does not
    exist already
    """
    home = expanduser("~")
    folder = home + awsfolder
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = home + awsconfigfile

    # If the credentials file exist under ./aws, then we do not need to create
    # a template
    if os.path.isfile(filename):
        return

    f = None
    bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    template_path = path.join(bundle_dir, 'template')
    env = Environment(
        loader=FileSystemLoader(
            str(template_path)),
        autoescape=True)

    myString = "[default] \n" \
               "aws_access_key_id = \n" \
               "aws_secret_access_key = \n"
    template = Environment(
        loader=BaseLoader(),
        autoescape=True).from_string(myString)
    output_from_template = template.render()
    try:
        f = open(filename, "w+")
        f.write(output_from_template)
    except IOError:
        track = traceback.format_exc()
        print(track)
        print("File not accessible")
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
    finally:
        if f is not None:
            f.close()


def get_aws_access(url, user, password, duration_seconds):
    """
    this function has been created to call the aws access
    module in batch
    :url : The url of the AWS account
    :user: The user id to connect to AWS
    :password: The password to connect to AWS
    :duration_seconds: Duration for which access is required.
    The default duration is 1 hour
    """

    try:
        saml_assertion = get_saml_assertion(url, user, password)
        create_default_profile()
        saml2AWS(saml_assertion, duration_seconds)
        return 0
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print("File not accessible")
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        return 1


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Retrieves and stores a temporary token which is used to access AWS resource")
    parser.add_argument('--awsurl',
                        dest='url',
                        type=str,
                        help=("Specify a valid aws url"),
                        required=False)

    parser.add_argument('--u',
                        dest='user',
                        type=str,
                        help=("Specify your userid"),
                        required=False)

    parser.add_argument('--p',
                        dest='password',
                        type=str,
                        help=("Specify your password"),
                        required=False)

    parser.add_argument(
        '--dur',
        dest='duration_seconds',
        type=str,
        help=(
            "Specify duration in seconds for which you need access."
            "Must be > 900 and less than 43200. Default is 1 hour or 3600 secs."),
        required=False)

    args = parser.parse_args()

    url = args.url
    user = args.user
    duration_seconds = args.duration_seconds

    if args.url is None:
        try:
            print("AWS url:", end='')
            url = input()
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
    else:
        url = args.url

    if args.user is None:
        try:
            print("Username:", end='')
            user = input()
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
    else:
        user = args.user

    if args.password is None:
        try:
            password = getpass.getpass()
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
    else:
        password = args.password

    try:
        get_aws_access(url, user, password, duration_seconds)
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
