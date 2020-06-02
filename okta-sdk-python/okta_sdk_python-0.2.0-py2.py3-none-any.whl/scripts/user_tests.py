import json
import random

from okta.UsersClient import UsersClient
from okta.models.user.User import User
from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from okta_class_extensions import ExtendedUser, ExtendedUserProfile
from script_config import base_url, api_token

# get a random int
start_number = random.randrange(1, 1000, 1)
end_number = random.randrange(1, 1000, 1)

usersClient = UsersClient(
    base_url=base_url, api_token=api_token, user_class=ExtendedUser)

user = ExtendedUser(
    login="testuser{0}@mailinator.com".format(start_number),
    firstName="Test",
    lastName="User {0}".format(start_number),
    middleName="David",
    honorificPrefix="Mr.",
    honorificSuffix="Sr.",
    email="testuser{0}@mailinator.com".format(start_number),
    title="Some sort of job title",
    displayName="Not automated",
    nickName="Testy{0}".format(start_number),
    profileUrl="http://localhost",
    secondEmail="testuser{0}@mailinator.com".format(end_number),
    mobilePhone="9135551212",
    primaryPhone="9145551213",
    streetAddress="123 Main Street",
    city="Anytown",
    state="KS",
    zipCode="12345",
    countryCode="US",
    postalAddress="Different than street address?",
    locale="en_US",
    timezone="US/Central",
    userType="Okta",
    employeeNumber="123455677890",
    costCenter="Finance & Operations",
    organization="Thorax Studios",
    division="Operations",
    department="Information Technology",
    managerId="0987654321",
    manager="Manny McManager",
    goals="Workout goals",
    sfdc_id="Salesforce ID",
    windows_username="WINLOGON"
)

print("Creating new user...")
print(json.dumps(user, cls=Serializer, indent=2))

try:
    test_user = usersClient.create_user(user, activate=False)
    uid = test_user.id
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
    exit(2)

user_id = test_user.id

print("Get User")
user = usersClient.get_user(user_id)
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print(json.dumps(user.profile, cls=Serializer, indent=2))
print("")

print("Update User-partial update")
updated_user = User(
    login=user.profile.login,
    firstName=user.profile.firstName,
    lastName="User {0}".format(end_number),
    email=user.profile.email
)
user = usersClient.update_user_by_id(uid, updated_user, True)
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print(json.dumps(user.profile, cls=Serializer, indent=2))
print("")


print("Update User-full update")
updated_user = User(
    login=user.profile.login,
    firstName=user.profile.firstName,
    lastName="User {0}".format(end_number),
    email=user.profile.email
)
user = usersClient.update_user_by_id(uid, updated_user, False)
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print(json.dumps(user.profile, cls=Serializer, indent=2))
print("")

# suspend a user
# only valid for a user that is ACTIVE
try:
    user = usersClient.suspend_user(uid)
    print("Suspend User")
    print("ID: {0}".format(user.id))
    print("Status: {0}".format(user.status))
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)

print("")

# deactivate a user
usersClient.deactivate_user(uid)
user = usersClient.get_user(uid)
print("Deactivate User")
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print("")

# delete a user
usersClient.delete_user(uid)
print("Delete User")
print("")

# try and get the user we just deleted
print("Try and get the user we just deleted")
try:
    user = usersClient.get_user(uid)
    print(json.dumps(user.profile, cls=Serializer, indent=2))
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
