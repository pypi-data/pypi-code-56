# EXIT CODES
success = 0
failure = 1
# MESSAGES
support_contact = "Please connect with the support team"
# ALL DUO CONSTANTS
sslverification = True
auth_url = "https://{duo_host}/frame/web/v1/auth"
prompt_url = "https://{duo_host}/frame/prompt"
status_url = "https://{duo_host}/frame/status"
result_url = "https://{duo_host}{duo_result_url}"
call_back_url = "{cisco_url}{duo_callback}?sig_response={sig_response}"
user_type = 'cco'
# AWS Params
awsfolder = '/.aws/'
awsconfigfile = '/.aws/credentials'
outputformat = 'json'
region = 'us-west-2'
# DUO OPTIONS
options = [
    'Send Me a Push,Duo+Push',
    'Call Me,Phone+Call',
    'SMS me a code,sms',
    'Passcode,Passcode']
