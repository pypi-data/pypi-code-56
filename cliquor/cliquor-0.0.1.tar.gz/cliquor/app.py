import sys
import argparse


class App:
    return_code=0
    parser=argparse.ArgumentParser()

    @classmethod
    def invoke(cls):
        cls().main()

    def tear_down(self):
        sys.exit(self.return_code)

    def handle_exception(self, exception):
        self.return_code = 1
        print('Error: %s' % exception, file=sys.stderr)

    def parse_arguments(self):
        self.register_version_argument()
        self.register_help_argument()

    def register_version_argument(self):
        self.parser.add_argument('--version', action='version',
                    version='%(prog)s v{}'.format(self.version))

    def register_help_argument(self):
        pass

    def register_commands(self):
        pass

    def execute(self):
        self.parser.parse_args()

    def main(self):
        try:
            self.parse_arguments()
            self.register_commands()
            self.execute()
        except Exception as e:
            self.handle_exception(e)
        finally:
            self.tear_down()
