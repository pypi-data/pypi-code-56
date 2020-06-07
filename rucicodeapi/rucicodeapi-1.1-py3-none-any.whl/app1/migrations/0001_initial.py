# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rootid', models.CharField(max_length=20)),
                ('mykey', models.CharField(max_length=20)),
                ('isdelete', models.BooleanField(default=False)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('setTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Keys',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rootid', models.CharField(max_length=20)),
                ('passwd', models.CharField(max_length=20)),
                ('money', models.IntegerField(max_length=20)),
                ('isdelete', models.BooleanField(default=False)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('setTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
