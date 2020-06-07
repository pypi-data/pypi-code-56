from setuptools import setup

setup(
    name='django-schedule-daemon',
    version='2020.6.6',
    install_requires=[
        'Django',
        'schedule',
        'setuptools',
    ],
    packages=[
        'django_schedule_daemon',
        'django_schedule_daemon.management',
        'django_schedule_daemon.management.commands',
    ],
)
