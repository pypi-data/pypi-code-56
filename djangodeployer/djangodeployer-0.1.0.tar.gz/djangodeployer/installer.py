#!/usr/bin/env python
import sys
import os
import subprocess
from shutil import copyfile
import json
from getpass import getpass
from pprint import pprint as pp

import logging
from logging.handlers import RotatingFileHandler
logging.basicConfig(format='%(message)s', datefmt= "%Y-%m-%d %H:%M:%S", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(RotatingFileHandler(filename='djangodeployer.log', mode='w', 
                  maxBytes=512000, backupCount=4))

class Djangodeployer:
    """
    A Class with all functions to deploy django
    """

    def __init__(self):
        self.configfile = 'dj_conf.json'
        self._IP_ADDRESS = None
        self._SERVER_NAME = None
        self._LINUX_USER = None
        self._DJ_PROJ = None
        self._PG_USER = None
        self._PG_DB = None
        self._DOMAIN_NAME = None
        self._VENV_PATH = None
        self._PROJ_PATH = None

    def run_command(self, command):
        "Listen for cmd commands and execute it"
        command = command.pop(0)
        list_commands = ['init', 'deploy', 'newuser']
        if command not in list_commands:
            logger.warning('ERROR: Unrecognised command.')
            sys.exit(1)
        elif command == 'init':
            self.cmd_init()
        elif command == 'deploy':
            self.run_full()
        elif command == 'newuser':
            self.create_user()

    def cmd_init(self):
        "Initialize default config file.in the current directory."
        if os.path.exists(self.configfile):
            logging.warning(f'File {self.configfile} already exists.')
            sys.exit(1)
        copyfile(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'default_conf.json'), 'dj_conf.json')
        logging.info(f'New file {self.configfile}')

    def read_config(self):
        with open('dj_conf.json') as config_file:
            CONFIG = json.load(config_file)
        self._IP_ADDRESS = CONFIG.get('IP_ADDRESS')
        self._SERVER_NAME = CONFIG.get('SERVER_NAME')
        self._LINUX_USER = os.getlogin()
        self._DJ_PROJ = CONFIG.get('DJ_PROJ')
        self._PG_USER = CONFIG.get('PG_USER')
        self._PG_DB = CONFIG.get('PG_DB')
        self._DOMAIN_NAME = CONFIG.get('DOMAIN_NAME')
        self._VENV_PATH = f'/home/{self._LINUX_USER}/{self._DJ_PROJ}/env/bin'
        self._PROJ_PATH = f'/home/{self._LINUX_USER}/{self._DJ_PROJ}/{self._DJ_PROJ}'

    def print_logo(self):
        init_string = r"""
        ____      _____    _   ____________
       / __ \    / /   |  / | / / ____/ __ \
      / / / /_  / / /| | /  |/ / / __/ / / /
     / /_/ / /_/ / ___ |/ /|  / /_/ / /_/ /
    /_____/\____/_/  |_/_/ |_/\____/\____/
        ____  __________  __    ______  ____________
       / __ \/ ____/ __ \/ /   / __ \ \/ / ____/ __ \
      / / / / __/ / /_/ / /   / / / /\  / __/ / /_/ /
     / /_/ / /___/ ____/ /___/ /_/ / / / /___/ _, _/
    /_____/_____/_/   /_____/\____/ /_/_____/_/ |_|
        """
        logger.warning(init_string)
        logger.info('Program started.')

    def run(self):
        pass

    def gprint(self, color, text):
        """
        Color print
        Input:
        ------------
        color: 'bg' - green; 'br' - red; 'bs' - grey
        text: text to be printed
        """
        if color == 'bg':
            logger.info(f'\033[1;32;48m{text}\033[0m')
        if color == 'br':
            logger.info(f'\033[1;31;48m{text}\033[0m')
        if color == 'bs':
            logger.info(f'\033[1;30;48m{text}\033[0m')

    def wrap_print(self, text):
        "Print with borders around the text"
        line_width = 80
        logger.info('=' + '=' * line_width + '=')
        logger.info(f'|{text:^{line_width}}|')
        logger.info('=' + '=' * (line_width) + '=')

    def execute(self, command):
        "Run bash command"
        self.gprint('bs', 'Running command   ' + command)
        result = os.system(command)
        if result == 0:
            self.gprint('bg', 'Successfully executed.')
        else:
            self.gprint('bg', f'Not succeed on {command}.')

    def install_packages(self):
        self.wrap_print('Install system dependencies.')
        self.execute('sudo apt-get update && sudo apt-get upgrade -y')
        self.execute('sudo apt-get install git curl wget build-essential \
                     nginx supervisor ufw python3 python3-pip python3-venv python3-dev -y')

    def check_root(self):
        if os.geteuid() == 0:
          logger.warning('Running as root user. Please run it as another user. This affects folders ownership.')
          sys.exit(1)

    def create_user(self):
        "Create superuser on the server with the LINUX_USER name"
        if self.ask_input(f"Create a new user {self._LINUX_USER}? y/n  "):
            self.wrap_print(f'Create superuser {self._LINUX_USER}.')
            self.execute(f'sudo adduser {self._LINUX_USER}')
            self.execute(f'sudo adduser {self._LINUX_USER} sudo')
            self.execute(f'sudo -su {self._LINUX_USER}')
            logging.info('New user created. Deploy with the new user.')

    def change_hostname(self):
        self.wrap_print('Changing serer hostname.')
        self.execute(f'sudo hostnamectl set-hostname {self._SERVER_NAME}')
        self.execute('hostname')

    def setup_firewall(self):
        self.wrap_print("Setup UFW firewall")
        self.execute('sudo apt-get install ufw')
        self.execute('sudo ufw default allow outgoing')
        self.execute('sudo ufw default deny incoming')
        self.execute('sudo ufw allow ssh')
        # self.execute('sudo ufw allow 8000')
        # self.execute('sudo ufw allow 5000')
        self.execute("sudo ufw allow 'Nginx Full'")
        self.execute('sudo ufw enable -y')
        self.execute('sudo ufw status')

    def ask_input(self, message: str):
        question = input(message)
        if question in ['y', 'yes', 'Y', 'Yes', 'YES']:
            return True
        elif question in ['n', 'no', 'N', 'No', 'NO']:
            return False
        else:
            self.ask_input(message)

    def create_django_proj_folder(self):
        self.wrap_print("Create Django Folder")
        main_dir = f'/home/{self._LINUX_USER}/{self._DJ_PROJ}'
        if os.path.exists(main_dir):
            if self.ask_input(f"Directory {main_dir} already exists. Completely erase it's content ? y/n "):
                self.execute(f'sudo rm -rf {main_dir}')
        self.execute(f'mkdir -p {main_dir}')

    def create_django_venv(self):
        self.wrap_print("Create Django venv")
        os.chdir(f"/home/{self._LINUX_USER}/{self._DJ_PROJ}")
        self.execute(f'python3 -m venv env')
        self.execute('pwd')
        self.execute(
            f'{self._VENV_PATH}/pip install django gunicorn psycopg2-binary')
        self.execute(f'{self._VENV_PATH}/python -m django --version')

    def check_venv(self):
        self.wrap_print("Checking venv")
        self.execute(f'{self._VENV_PATH}/pip freeze')

    def create_django_proj(self):
        self.wrap_print("Create Django project")
        os.chdir(f"/home/{self._LINUX_USER}/{self._DJ_PROJ}")
        self.execute(f'{self._VENV_PATH}/django-admin startproject {self._DJ_PROJ}')

    def edit_allowed_hosts(self):
        self.wrap_print("Edit allowed hosts on django project")
        filename = f"{self._PROJ_PATH}/{self._DJ_PROJ}/settings.py"
        text = open(filename).read()
        open(filename, "r+").write(text.replace("ALLOWED_HOSTS = []",
                                                f"ALLOWED_HOSTS = ['{self._IP_ADDRESS}']"))
        open(filename, "a").write(
            "\nSTATIC_ROOT = os.path.join(BASE_DIR, 'static')\n")
        logger.info(f'Django config file overwrited.')

    def collect_statics(self):
        """
        Running only:
        - 'python manage.py migrate',
        - 'python manage.py collectstatic',
    --------------------------------------------

        for documentations example:
        'pip install gunicorn psycopg2-binary',
        'python manage.py makemigrations',
        'python manage.py migrate',
        'python manage.py createsuperuser',
        'python manage.py collectstatic',
        """
        self.wrap_print("Generate static files on the django project")
        os.chdir(self._PROJ_PATH)
        self.execute(f'{self._VENV_PATH}/python manage.py collectstatic')
        self.execute(f'{self._VENV_PATH}/python manage.py migrate')
        logging.info('Finished with generating statics')

    def set_supervisor_gunicorn_proccess(self):
        # supervisor
        # sudo mkdir -p /var/log/djangosite
        # sudo nano /etc/supervisor/conf.d/djangosite.conf
        # sudo touch /var/log/djangosite/djangosite.err.log
        # sudo touch /var/log/djangosite/djangosite.out.log
        # sudo supervisorctl status
        # sudo supervisorctl reload
        """
        [program:djangosite]
        directory=/home/hm/djangosite/djangosite
        command=/home/hm/djangosite/env/bin/gunicorn -w 3 djangosite.wsgi:application
        user=hm
        autostart=true
        autorestart=true
        stopasgroup=true
        killasgroup=true
        stderr_logfile=/var/log/djangosite/djangosite.err.log
        stdout_logfile=/var/log/djangosite/djangosite.out.log
        group=www-data
        environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
        """
        self.wrap_print("Create a supervisor process to run gunicorn")
        self.execute(f'sudo mkdir -p /var/log/{self._DJ_PROJ}')
        self.execute(f'sudo touch /var/log/djangosite/{self._DJ_PROJ}.err.log')
        self.execute(f'sudo touch /var/log/djangosite/{self._DJ_PROJ}.out.log')
        filename = f'/etc/supervisor/conf.d/{self._DJ_PROJ}.conf'
        SUPERVISOR_CONF = (
            f'[program:{self._DJ_PROJ}]\n',
            f'directory={self._PROJ_PATH}\n',
            f'command={self._VENV_PATH}/gunicorn -w 3 {self._DJ_PROJ}.wsgi:application\n',
            f'user={self._LINUX_USER}\n',
            f'autostart=true\n',
            f'autorestart=true\n',
            f'stopasgroup=true\n',
            f'killasgroup=true\n',
            f'stderr_logfile=/var/log/{self._DJ_PROJ}/{self._DJ_PROJ}.err.log\n',
            f'stdout_logfile=/var/log/{self._DJ_PROJ}/{self._DJ_PROJ}.out.\n',
            f'group=www-data\n',
            f'environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8\n'
        )
        SUPERVISOR_CONF = "".join(SUPERVISOR_CONF)
        SUPERVISOR_CONF = "'" + SUPERVISOR_CONF + "'"
        self.execute(f'sudo bash -c "echo {SUPERVISOR_CONF} > {filename}"')
        self.execute('sudo supervisorctl reload')
        self.execute('sudo supervisorctl status')

    def set_nginx(self):
        """
        # Nginx acts as a reverse proxy. It's very fast for serving static files.
        # Also redirects to gunicorn to handle the python code when needed.
        # NGINX
        # sudo nano /etc/nginx/sites-enabled/djangosite
        # sudo nginx -t
        # sudo systemctl restart nginx
        -------------
        server {
            listen 80;
            server_name 146.28.50.56;
            location /static {
                alias /home/hm/djangosite/djangosite/static;
            }
            location / {
                proxy_pass http://localhost:8000/;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
            }
        }
        -------------
        #FOR MULTIPLE APPLICATIONS
        location / foo {
                proxy_pass http: // localhost: 3200 /
            }

    Notice the additional / at the end of the proxy_pass directive.
    NGINX will strip the matched prefix / foo and pass the remainder to the backend server at the URI / .
    Therefore, http: // myserver: 80/foo/bar will post to the backend at http: // localhost: 3200/bar
        """
        self.wrap_print("Create NGINX config file")
        self.execute('sudo rm -rf /etc/nginx/site-enabled/default')
        filename = f'/etc/nginx/sites-enabled/{self._DJ_PROJ}'
        self.execute(f'sudo touch {filename}')
        self.gprint('bg', 'Your IP address is:')
        self.execute('curl -4 ifconfig.co')
        self.gprint('bg', 'Your IP address is:')
        self.execute('curl    http://ifconfig.me/ip')
        NGINX_CONFIG = (
            'server {\n',
            '    listen 80;\n',
            f'    server_name {self._DOMAIN_NAME};\n',
            '\n',
            '    location /static {\n',
            f'        alias /home/{self._LINUX_USER}/{self._DJ_PROJ}/{self._DJ_PROJ}/static;\n',
            '    }\n',
            '\n',
            '    location / {\n',
            '        proxy_pass http://localhost:8000/;\n',
            '        include /etc/nginx/proxy_params;\n',
            '        proxy_redirect off;\n',
            '    }\n',
            '}\n',
        )
        NGINX_CONFIG = "".join(NGINX_CONFIG)
        NGINX_CONFIG = "'" + NGINX_CONFIG + "'"
        self.execute(f'sudo bash -c "echo {NGINX_CONFIG} > {filename}"')
        self.execute('sudo nginx -t')
        if self.ask_input('Restart NGINX service y/n ? '):
            self.execute('sudo systemctl restart nginx')

    def set_certbot_ssl(self):
        self.wrap_print('Install SSL certificates on the server')
        self.gprint(
            'br', 'Visit https://zerossl.com if you need certificate for IP address\n')
        self.gprint(
            'bs', 'Easiest way for SSL cert is certbot, but requires domain name.')
        if self.ask_input(f'Please confirm your domain name {self._DOMAIN_NAME} - y/n? '):
            self.execute('sudo apt-get install certbot python-certbot-nginx')
            self.execute(f'sudo certbot --nginx -d {self._DOMAIN_NAME}')
            self.execute('sudo certbot renew --dry-run')
            self.gprint('bs', """
                The jrontab commands should be in:
                /etc/crontab/
                /etc/cron.*/*
                systemctl list-timers
            """)
            self.execute('sudo systemctl list-timers')

    def adjust_rights(self):
        self.wrap_print('Changing file and folder permissions.')
        if self.ask_input('Make migrations on sqlite3 db - y/n?'):
            self.execute(f'sudo chown :www-data {self._PROJ_PATH}/db.sqlite3')
            self.execute(f'sudo chmod 664 {self._PROJ_PATH}/db.sqlite3')
        self.execute(f'sudo chown :www-data {self._PROJ_PATH}')
        self.execute(f'sudo mkdir -p {self._PROJ_PATH}/media/')
        self.execute(f'sudo chown -R :www-data {self._PROJ_PATH}/media/')
        self.execute(f'sudo chmod -R 775 {self._PROJ_PATH}/media/')
        self.execute(f'sudo chmod 775 {self._PROJ_PATH}')
        self.execute(f'ls -la {self._PROJ_PATH}')

    def set_db_to_postgres(self):
        self.wrap_print('Install PostgreSQL Database')
        if self.ask_input('Install postgresql database y/n? '):
            if self.ask_input('Install also PostGIS extension for GeoDjango - y/n? '):
                self.execute('sudo apt-get install postgis')
            else:
                self.execute('sudo apt-get install libpq-dev postgresql postgresql-contrib')
                self.create_postgresdb()
        else:
            self.gprint('bs', 'Skipping Postgresql....')

    def create_postgresdb(self):
        self.wrap_print('Create database for Django in PostgreSQL.')
        PG_PASS = getpass('Please enter password')
        PG_PASS2 = getpass('Please confirm password')
        while PG_PASS != PG_PASS2:
            logging.warning("Passwords don't match! Please try again...")
            PG_PASS = getpass('Please enter password')
            PG_PASS2 = getpass('Please confirm password')

        process = subprocess.Popen(
            ["sudo", "-u", "postgres", "psql"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
            universal_newlines=True,
        )
        process.stdin.write("CREATE DATABASE " + self._PG_DB + ";")
        process.stdin.write("CREATE USER " + self._PG_USER + " WITH PASSWORD '" + PG_PASS + "';")
        process.stdin.write("ALTER ROLE " + self._PG_USER + " SET client_encoding TO 'utf8';")
        process.stdin.write("ALTER ROLE " + self._PG_USER + " SET default_transaction_isolation TO 'read committed';")
        process.stdin.write("ALTER ROLE " + self._PG_USER + " SET timezone TO 'UTC';")
        process.stdin.write("GRANT ALL PRIVILEGES ON DATABASE " + self._PG_DB + " TO " + self._PG_USER + ";")
        process.stdin.write(r"\q")
        output, errors = process.communicate()
        self.gprint('bg', output)
        self.gprint('br', errors)

    def run_full(self):
        self.print_logo()
        self.read_config()
        self.check_root()
        self.change_hostname()
        self.install_packages()
        self.setup_firewall()
        self.create_django_proj_folder()
        self.create_django_venv()
        self.check_venv()
        self.create_django_proj()
        self.edit_allowed_hosts()
        self.collect_statics()
        self.adjust_rights()
        self.set_db_to_postgres()
        self.set_supervisor_gunicorn_proccess()
        self.set_nginx()
        self.set_certbot_ssl()
