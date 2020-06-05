import boto3

from pprint import pprint
from bullet import Bullet, Input, styles, VerticalPrompt, Check, YesNo

r53domains = boto3.client('route53domains')

def get_user_picked_domains_to_change():
    # List Route 53 domains
    response = r53domains.list_domains()
    domain_list = []
    for domain in response["Domains"]:
        domain_list.append(domain["DomainName"])
    # Prompt user to pick which domains they want
    domains = Check(
        "Which domains would you like to update? (Press space to (de)select a domain)", 
        choices=domain_list,
    ).launch()
    print("\nYou selected:")
    for d in domains:
        print(d)
    print("\n")
    return domains


def get_contact_details():
    contact_info = VerticalPrompt(
        [
            Input("First Name: "),
            Input("Last name: "),
            Bullet(
                prompt = "Choose a contact type from the items below: ", 
                choices = ['PERSON', 'COMPANY', 'ASSOCIATION', 'PUBLIC_BODY', 'RESELLER'],
                **styles.Ocean
            ),
            Input(
                "Organization name (Used when contact type is not a person): ", 
                pattern=".*"
            ),
            Input("Address Line 1: "),
            Input("Address Line 2: "),
            Input("City: "),
            Input("State: "),
            Input(
                "Two Digit Country Code (e.g. US, GB, JP): ",
                pattern="^[A-Z]{2}$"),
            Input("Zip Code: "),
            Input(
                "Phone Number with period after country code (e.g. for United States: +1.5556667788): ",
                pattern="^\+[0-9]{1,2}\.[0-9]{10}$"
            ),
            Input("Email: ")
        ],
        spacing = 1
    ).launch()
    details = {
        'FirstName': contact_info[0][1],
        'LastName': contact_info[1][1],
        'ContactType': contact_info[2][1],
        'AddressLine1': contact_info[4][1],
        'AddressLine2': contact_info[5][1],
        'City': contact_info[6][1],
        'State': contact_info[7][1],
        'CountryCode': contact_info[8][1],
        'ZipCode': contact_info[9][1],
        'PhoneNumber': contact_info[10][1],
        'Email': contact_info[11][1],
    }
    if details['ContactType'] != "PERSON":
        details["OrganizationName"] = contact_info[3][1]
    return details


def update_domains(selected_domains, contact_details):
    # Show the domains and details and have the user confirm
    print("Your contact information will be updated to the following: ")
    print("\n")
    pprint(contact_details)
    print("\n")
    if not YesNo("Does the above look correct? (y/n) ").launch():
        print("Ok! Go ahead and try again.")
        return
    print("The domains to be updated are: ")
    for domain in selected_domains:
        print(domain)
    print("\n")
    if not YesNo("Does the above look correct? (y/n) ").launch():
        print("Ok! Go ahead and try again.")
        return
    for domain in selected_domains:
        result = r53domains.update_domain_contact(
            DomainName=domain,
            AdminContact=contact_details,
            RegistrantContact=contact_details,
            TechContact=contact_details
        )


def main():
    domains = get_user_picked_domains_to_change()
    details = get_contact_details()
    update_domains(domains, details)
    print("Domain contact details updated!")

if __name__ == "__main__":
    main()
