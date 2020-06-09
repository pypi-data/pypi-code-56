import os
import argparse
import shutil

from git import Repo
from template_library.library_tools import LibraryTools
import zipfile
import tarfile
import requests
import json
import io, zipfile
import sys
import logging

library_tools = LibraryTools()
env_path = os.getenv("HOME") + "/.config/template_library"
templates_types = {"data_types": 1, "artifact_types": 2, "capability_types": 3, "requirement": 4, "relationship_types": 5, "interface_types": 6, "node_types": 7,
                   "group": 8, "policy_types": 9, "csar": 10, "other": 11}
templates_type_names = {"data_types": "DataType", "artifact_types": "ArtifactType", "capability_types": "CapabilityType",
                        "requirement": "Requirement", "relationship_types": "RelationshipType",
                        "interface_types": "InterfaceType", "node_types": "NodeType",
                   "group": "Group", "policy_types": "PolicyType", "csar": "Csar", "other": "Other"}


def add_entity_template(node_type_path, args, api_address, headers):
    files = []
    if os.path.isdir(node_type_path):
        node_file_list = []
        for node_subdir, node_dirs, node_files in os.walk(node_type_path):
            for file in node_files:
                node_file_list.append(file)
                if ".yml" in str(file):
                    files.append(('implementation_file', open(args.path + "/files/" + str(file), 'rb')))
                if ".tosca" in str(file):
                    files.append(('template_file', open(args.path + "/" + str(file), 'rb')))

        implementation = any('.yml' in x for x in node_file_list)
        definition = any('.tosca' in x for x in node_file_list)
        if not implementation:
            print("Implementation missing for " + node_type_path + "\n")
        if not definition:
            print("Definition missing for " + node_type_path + "\n")

        name, group, template_type = get_name_type(node_type_path)
        template_id = add_template(api_address, args, headers, group, templates_types[template_type])

        add_version(api_address, args, headers, files, template_id)

    elif tarfile.is_tarfile(os.path.normpath(node_type_path)) or zipfile.is_zipfile(os.path.normpath(node_type_path)):
        print("Entity template can only be uploaded as a directory.")


def add_service_template(node_type_path, args, api_address, headers):
    files = []
    if os.path.isdir(node_type_path):
        print("Service template can only be uploaded in tar or zip format.")
    elif tarfile.is_tarfile(os.path.normpath(node_type_path)) or zipfile.is_zipfile(os.path.normpath(node_type_path)):
        zip_file = ('template_file', open(node_type_path, 'rb'))
        files.append(zip_file)

        template_id = add_template(api_address, args, headers, "node.blueprint", 10)
        add_version(api_address, args, headers, files, template_id)


def add_version(api_address, args, headers, files, template_id):
    api_url = api_address + "/api/versions"

    data = {
        "template_id": template_id,
        "version": args.version
    }

    headers.pop("Content-type")
    try:
        response = requests.Session().post(api_url, headers=headers, data=data, files=files)
        response.raise_for_status()
        print("New template version created!")
    except requests.HTTPError as e:
        logging.debug(e)
        print(e.response.content.decode("utf-8"))
        exit(1)


def add_template(api_address, args, headers, group, node_type_id):
    api_url = api_address + "/api/templates"
    access = args.public_access
    # TODO: if template already exists and you want to make in public as well you have to give a new name
    data = {
        "shorthand_name": args.name,
        "type_uri": group,
        "template_type_id": node_type_id,
        "public_access": str(access)
    }

    headers = authorization(headers)

    try:
        response = requests.post(api_url, data=str(data), headers=headers)
        response.raise_for_status()
        template_id = json.loads(response.content.decode("utf-8"))["object_id"]
    except requests.HTTPError as e:
        logging.debug(e)
        print(e.response.content.decode("utf-8"))
        if e.response.status_code == 406:
            api_url = api_address + "/api/templates/name/" + args.name
            try:
                response = requests.get(api_url, headers=headers)
                template_id = json.loads(response.content.decode("utf-8"))["id"]
                response.raise_for_status()
            except requests.HTTPError as e:
                logging.debug(e)
                print(e.response.content.decode("utf-8"))
    return template_id


def download_template(args, api_address, headers):
    api_url = api_address + "/api/versions/files/" + args.version_id
    headers = authorization(headers)
    # TODO: save files in appropriate folders
    try:
        response = requests.get(api_url, headers=headers)
        # TODO: check if response is zip
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(path=args.path)
        response.raise_for_status()
    except requests.HTTPError as e:
        logging.debug(e)
        print(e.response.content.decode("utf-8"))
        exit(1)


def list_templates(args, api_address, headers):
    access = args.public_access
    headers = authorization(headers)

    if access:
        #api_url = api_address + "/api/templates"
        api_url = api_address + "/api/templates/template_type/" + "10"

    else:
        file = open(env_path + "/.username", "r")
        env_username = file.read()
        file.close()

        api_url = api_address + "/api/templates/user/name/" + env_username

    try:
        response = requests.get(api_url, headers=headers)
        if len(json.loads(response.content.decode("utf-8"))) != 0:
            for i in json.loads(response.content.decode("utf-8")):
                if not args.name:
                    format_output(i)
                elif i["shorthandName"] == args.name:
                    format_output(i)
        response.raise_for_status()
    except requests.HTTPError as e:
        logging.debug(e)
        print(e.response.content.decode("utf-8"))
        exit(1)


def format_output(output):
    for key, value in output.items():
        print(key + ": " + str(value))
    print()


def list_versions(args, api_address, headers):
    if args.template_id:
        api_url = api_address + "/api/versions/template/" + args.template_id
    if args.template_name:
        api_url = api_address + "/api/versions/template/name/" + args.template_name

    headers = authorization(headers)
    try:
        response = requests.get(api_url, headers=headers)
        if len(json.loads(response.content.decode("utf-8"))) != 0:
            for i in json.loads(response.content.decode("utf-8")):
                format_output(i)
        response.raise_for_status()
    except requests.HTTPError as e:
        logging.debug(e)
        print(e.response.content.decode("utf-8"))
        exit(1)


def authorization(headers):
    try:
        file = open(env_path + "/.token", "r")
        env_token = file.read()
        file.close()
        if not env_token:
            print("Please log in.")
        else:
            headers["Authorization"] = "Bearer " + env_token
    except Exception as e:
        logging.debug(e)
        print("Please log in.")
        exit(1)
    return headers


def get_artifact_warnings():
    return library_tools.get_warnings_log()


def get_definition(node_type_path):
    node_file_list = []
    for node_subdir, node_dirs, node_files in os.walk(node_type_path):
        for file in node_files:
            node_file_list.append(file)
            if '.tosca' in file:
                return file


def get_name_type(node_type_path):
    node_type_path += "/" + get_definition(node_type_path)
    data_dict = library_tools.implementation_to_dictionary(node_type_path)
    template_type = list(data_dict.keys())[1]
    group, name = list(data_dict[template_type].keys())[0].rsplit('.', 1)
    return name, group, template_type


def store_true():
    return True


def login_user(api_address, headers, username, password):
    api_url = api_address + "/api/auth/login"
    logging.debug(api_url)
    data = {
        "username": username,
        "password": password
    }
    logging.debug(username)
    logging.debug(password)
    try:
        response = requests.post(api_url, data=str(data), headers=headers)
        response.raise_for_status()
        token = json.loads(response.text)["token"]
        logging.debug(response.text)
        return token
    except requests.HTTPError as e:
        logging.debug(e)
        print(e.response.content.decode("utf-8"))
        exit(1)


def main():
    parser = argparse.ArgumentParser()

    command_options = parser.add_subparsers(dest='command')

    service_templates = command_options.add_parser('service-template', help='Edit a service template.')
    service_template_options = service_templates.add_subparsers(dest='template_options')
    save_service = service_template_options.add_parser('save', help='Save a template to database.')
    get_service = service_template_options.add_parser('get', help='Get a template from database.')
    list_service_parser = service_template_options.add_parser('list', help='List templates from database.')
    version_service_parser = service_template_options.add_parser('version', help='Version options for templates.')

    version_service_options = version_service_parser.add_subparsers(dest='version_options')
    list_service_version = version_service_options.add_parser('list', help='List versions of a template from database.')
    list_service_version_group = list_service_version.add_mutually_exclusive_group(required=True)
    list_service_version_group.add_argument('--template_id', help='Id of the template.', dest='template_id')
    list_service_version_group.add_argument('--template_name', help='Name of the template.', dest='template_name')

    save_service.add_argument('--name', help='Name of the template.', dest='name', required=True)
    save_service.add_argument('--path', help='Path to the template code or desired template location.', dest='path',
                             required=True)
    save_service.add_argument('--public_access', help='Is template available to the public or just this account',
                             dest='public_access', action="store_true", default=False)
    save_service.add_argument('--version', help='Version of the template to upload/download',
                             dest='version', required=True)

    get_service.add_argument('--version_id', help='Id of the template.', dest='version_id', required=True)
    get_service.add_argument('--path', help='Path to the template code or desired template location.', dest='path',
                            required=True)
    get_service.add_argument('--public_access', help='Is template available to the public or just this account',
                            dest='public_access', action="store_true", default=False)

    list_service_parser.add_argument('--name', help='Name of the template.', dest='name')
    list_service_parser.add_argument('--public_access', help='Is template available to the public or just this account',
                                    dest='public_access', action="store_true", default=False)

    entity_templates = command_options.add_parser('entity-template', help='Edit an entity template.')
    entity_template_options = entity_templates.add_subparsers(dest='template_options')
    save_entity = entity_template_options.add_parser('save', help='Save a template to database.')
    get_entity = entity_template_options.add_parser('get', help='Get a template from database.')
    list_entity_parser = entity_template_options.add_parser('list', help='List templates from database.')
    version_entity_parser = entity_template_options.add_parser('version', help='Version options for templates.')

    version_entity_options = version_entity_parser.add_subparsers(dest='version_options')
    list_entity_version = version_entity_options.add_parser('list', help='List versions of a template from database.')
    list_entity_version_group = list_entity_version.add_mutually_exclusive_group(required=True)
    list_entity_version_group.add_argument('--template_id', help='Id of the template.', dest='template_id')
    list_entity_version_group.add_argument('--template_name', help='Name of the template.', dest='template_name')

    save_entity.add_argument('--name', help='Name of the template.', dest='name', required=True)
    save_entity.add_argument('--path', help='Path to the template code or desired template location.', dest='path',
                      required=True)
    save_entity.add_argument('--public_access', help='Is template available to the public or just this account',
                      dest='public_access', action="store_true", default=False)
    save_entity.add_argument('--version', help='Version of the template to upload/download',
                      dest='version', required=True)

    get_entity.add_argument('--version_id', help='Id of the template.', dest='version_id', required=True)
    get_entity.add_argument('--path', help='Path to the template code or desired template location.', dest='path',
                     required=True)
    get_entity.add_argument('--public_access', help='Is template available to the public or just this account',
                     dest='public_access', action="store_true", default=False)

    list_entity_parser.add_argument('--name', help='Name of the template.', dest='name')
    list_entity_parser.add_argument('--public_access', help='Is template available to the public or just this account',
                             dest='public_access', action="store_true", default=False)

    setup = command_options.add_parser('setup', help='Setup client variables.')

    login = command_options.add_parser('login', help='Login to your account.')
    login.add_argument('--username', help='Username of the user.', dest='username', required=True)
    login.add_argument('--password', help='Password of the user.', dest='password', required=True)

    logout = command_options.add_parser('logout', help='Logout of your account.')

    # TODO: we could also have a validate-model
    create_model = command_options.add_parser('create-model', help='Initialize a model directory and files.')

    create_blueprint = command_options.add_parser('create-blueprint',
                                                  help='Initialize a blueprint directory and files.')

    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Metadata storage: ' + env_path)

    if not len(sys.argv) > 1:
        parser.print_help()

    headers = {"Content-type": "application/json"}

    if args.command == "setup":
        try:
            os.mkdir(env_path)
        except Exception as e:
            logging.debug(e)
        api_endpoint = input("Enter API endpoint (https://host:port):")

        data = {
            "username": "test",
            "password": "test"
        }
        try:
            response = requests.post(api_endpoint + "/api/auth/login", data=str(data), headers=headers)
            response.raise_for_status()
        except requests.HTTPError as e:
            logging.debug(len(e.response.content.decode("utf-8")))
            logging.debug(e.response.content.decode("utf-8"))
            logging.debug(e.response.status_code)
            if len(e.response.content.decode("utf-8")) == 0 and e.response.status_code != 201:
                print("Wrong endpoint")
        except requests.exceptions.ConnectionError as con:
            logging.debug(con)
            print("Wrong endpoint")

        logging.debug(env_path + "/.endpoint")
        file_endpoint = open(env_path + "/.endpoint", "w")
        file_endpoint.write(api_endpoint)
        file_endpoint.close()

    try:
        file = open(env_path + "/.endpoint", "r")
        api_address = file.read()
        logging.debug(api_address)
        file.close()
    except Exception as e:
        logging.debug(e)
        print("Please run xopera-template-library setup first to configure API endpoint.")
        exit(1)

    if args.command == "register":
        api_url = api_address + "/api/auth/register"
        data = {
            "full_name": args.full_name,
            "username": args.username,
            "email": args.email,
            "password": args.password
        }
        try:
            response = requests.post(url=api_url, data=str(data), headers=headers)
            response.raise_for_status()
        except requests.HTTPError as e:
            logging.debug(e)
            print(e.response.content.decode("utf-8"))

    if args.command == "login":
        token = login_user(api_address, headers, args.username, args.password)

        file_token = open(env_path + "/.token", "w")
        file_token.write(token)
        file_token.close()

        file_username = open(env_path + "/.username", "w")
        file_username.write(args.username)
        file_username.close()
        print("User " + args.username + " logged in.")

    if args.command == "logout":
        shutil.rmtree(env_path)

    if args.command == "create-model":
        model_name = input("Model name:")
        model_type = input("Model type:")
        if model_type not in templates_types:
            print("Template type doesn't exist. Choose from: " + str(templates_types.keys()))
            exit(1)
        try:
            os.mkdir(model_name)
            open(model_name + "/" + templates_type_names[model_type] + ".tosca", 'a').close()

            model_name += "/files"
            os.mkdir(model_name)
            open(model_name + "/create.yml", 'a').close()

        except Exception as e:
            logging.debug(e)

    if args.command == "create-blueprint":
        blueprint_name = input("Blueprint name:")
        try:
            os.mkdir(blueprint_name)
            open(blueprint_name + "/ServiceTemplate.tosca", 'a').close()
        except Exception as e:
            logging.debug(e)

    if args.command == "entity-template":
        if args.template_options == "save":
            add_entity_template(args.path, args, api_address, headers)
        if args.template_options == "get":
            download_template(args, api_address, headers)
        if args.template_options == "list":
            list_templates(args, api_address, headers)
        if args.template_options == "version":
            if args.version_options == "list":
                list_versions(args, api_address, headers)

    if args.command == "service-template":
        if args.template_options == "save":
            add_service_template(args.path, args, api_address, headers)
        if args.template_options == "get":
            download_template(args, api_address, headers)
        if args.template_options == "list":
            list_templates(args, api_address, headers)
        if args.template_options == "version":
            if args.version_options == "list":
                list_versions(args, api_address, headers)