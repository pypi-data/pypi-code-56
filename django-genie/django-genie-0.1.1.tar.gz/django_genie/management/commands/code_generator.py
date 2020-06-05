from django.core.management.base import BaseCommand

from django_genie.code_generator import CodeGenerator


class Command(BaseCommand):
    help = 'Code Generator'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str)
        parser.add_argument('template', type=str)

    def handle(self, *args, **options):
        CodeGenerator(options['app'], options['template']).output()
