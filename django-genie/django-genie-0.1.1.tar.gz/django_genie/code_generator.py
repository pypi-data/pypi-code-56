import os
from django.template import Context, Engine

from .models import Models

CRUD_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
project = "" # Add your django project name


class CodeGenerator:
    def __init__(self, app, template):
        self.app = app
        self.template = template

    def output(self):
        """Prints out the generated code"""
        engine = Engine(
            debug=True,
            dirs=[os.path.join(CRUD_BASE_DIR, "templates")],
            libraries={
                'code_generator_tags': "templatetags.code_generator_tags"
            }
        )

        template = engine.get_template(self.template + ".py")
        print(template.render(Context({'models': Models(self.app).models, 'app': self.app})))
