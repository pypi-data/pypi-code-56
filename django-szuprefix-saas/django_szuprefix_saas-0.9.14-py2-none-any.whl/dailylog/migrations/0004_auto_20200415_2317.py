# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-04-15 23:17
from __future__ import unicode_literals

from django.db import migrations, models

def update_owner_name_and_user_name(apps, schema_editor):
    Record = apps.get_model('dailylog', 'Record')
    for r in Record.objects.filter(user_name=''):
        r.save()
        print r.id


class Migration(migrations.Migration):

    dependencies = [
        ('dailylog', '0003_auto_20200317_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='owner_group',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='\u5c5e\u4e3b\u5206\u7ec4'),
        ),
        migrations.AddField(
            model_name='record',
            name='owner_name',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='\u5c5e\u4e3b\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='record',
            name='user_group',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='\u7528\u6237\u5206\u7ec4'),
        ),
        migrations.AddField(
            model_name='record',
            name='user_name',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='\u7528\u6237\u59d3\u540d'),
        ),
        # migrations.RunPython(update_owner_name_and_user_name)
    ]
