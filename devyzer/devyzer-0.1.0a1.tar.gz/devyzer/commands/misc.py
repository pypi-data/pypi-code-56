import json

from halo import Halo
from project_configuration import schemaobject
from project_configuration.from_schema import DevyzerConfiguration
from questionary import prompt

from devyzer.commands.__init__ import Command
from devyzer.utils import EmptyValidator, print_with_color, bcolors


class DbSchemaCommand(Command):
    questions = [

        {
            'type': 'input',
            'name': 'db_host',
            'message': 'DB HOST',
            'validate': EmptyValidator,
            'default': '127.0.0.1',
        },
        {
            'type': 'input',
            'name': 'db_port',
            'message': 'DB PORT',
            'validate': EmptyValidator,
            'default': '3306',
        },
        {
            'type': 'input',
            'name': 'db_name',
            'message': 'DB NAME',
            'validate': EmptyValidator

        },
        {
            'type': 'input',
            'name': 'db_username',
            'message': 'DB USERNAME',
            'validate': EmptyValidator,
            'default': 'root'

        },
        {
            'type': 'password',
            'name': 'db_password',
            'message': 'DB PASSWORD',
            'validate': EmptyValidator,
            'default': 'root'

        },

        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Are you sure?'
        }
    ]

    def name(self):
        return "get-db-schema"

    def run(self, args, sio, project_configuration):
        print_with_color("enter your DB info:", bcolors.OKGREEN)
        answers = prompt(self.questions)
        confirm = answers.get("confirm")
        with Halo(text='Loading Schema ...', text_color='cyan', color='cyan', spinner='dots') as sp:
            try:
                if confirm is True:
                    url = self._url(answers)
                    schema = schemaobject.get_schema(url)
                    devyzer_config = DevyzerConfiguration()
                    devyzer_config.from_schema(schema)
                    config = devyzer_config.to_dict()
                    sp.succeed("project configuration is loaded")
                    sio.emit('user_uttered',
                             {"message": '/incoming_configuration',
                              'metadata': {
                                  'configurations': config
                              }})
                    # sio.emit('user_uttered',
                    #          {"message": '/incoming_configuration{"data":' + configuration + '}', 'metadata': {
                    #              'configurations': config
                    #          }})

            except Exception as e:
                sp.fail("Error: " + str(e))
                return False

        return True

    @staticmethod
    def _url(answers):
        return 'mysql://' + answers['db_username'] + ':' + answers['db_password'] + '@' + answers[
            'db_host'] + ':' + answers['db_port'] + '/' + answers['db_name']
