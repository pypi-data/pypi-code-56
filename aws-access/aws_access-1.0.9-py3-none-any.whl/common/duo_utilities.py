import ast
import re

from aws_access_util.constants import constants


def get_payload(form_response_soup, user_name, password):
    '''
    :param form_response_soup: The response returned after calling the url
    :param user_name: user name entered from cli
    :param password: password entered from cli
    :return: the payload for the next call
    '''
    payload = {}
    for inputtag in form_response_soup.find_all(re.compile('(INPUT|input)')):
        name = inputtag.get('name', '')
        value = inputtag.get('value', '')
        if "pf.username" in name.lower():
            # In the response this is the field for username
            payload[name] = user_name
        elif "email" in name.lower():
            # In the response this is the field for email, but this is not used
            payload[name] = user_name
        elif "pf.usertype" in name.lower():
            payload[name] = constants.user_type
        elif "pf.pass" in name.lower():
            # In the response this is the field for password
            payload[name] = password
        else:
            # Populate the parameter with the existing value (gets the hidden
            # fields in the login form)
            payload[name] = value
    return payload


def get_action_url(form_response_soup):
    '''
    :param form_response_soup: The response after calling the
    action url from the initial response
    :return: gets the auth form to be submitted next
    '''
    auth_form_submit_url = ''
    for input_tag in form_response_soup.find_all(re.compile('(FORM|form)')):
        action = input_tag.get('action')
        loginid = input_tag.get('id')
        if (action and loginid == "login-form"):
            auth_form_submit_url = action

    return auth_form_submit_url


def get_duo_attributes(form_response_soup):
    '''

    :param form_response_soup: response after submitting the auth url
    :return: the duo host name, signature and call back from duo init
    '''
    input_tag = form_response_soup.find_all(
        'script', {"type": "application/javascript"})
    duo_init = ast.literal_eval(
        input_tag[1].get_text().split(
            '(', 1)[1].split(')')[0])
    duo_host = duo_init['host']
    duo_signatures = duo_init['sig_request'].split(":")
    duo_callback = duo_init['post_action']

    return duo_host, duo_signatures, duo_callback


def get_duo_sid(form_response_soup):
    '''
    :param form_response_soup: response from auth url
    :return: gets the duo sid
    '''
    duo_sid = form_response_soup.find("input", {"name": "sid"})['value']
    return duo_sid


def get_assertion(form_response_soup):
    '''
    :param form_response_soup: response from the the final submission
    :return: sml assertion, this is what is used to connect to aws
    to get the temp token
    '''
    assertion = ''
    for input_tag in form_response_soup.find_all('input'):
        if (input_tag.get('name') == 'SAMLResponse'):
            # print(inputtag.get('value'))
            assertion = input_tag.get('value')
    return assertion
