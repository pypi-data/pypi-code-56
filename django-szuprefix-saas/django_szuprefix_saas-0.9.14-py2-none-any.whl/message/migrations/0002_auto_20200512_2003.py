# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-05-12 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u6709\u6548'),
        ),
        migrations.AddField(
            model_name='task',
            name='is_sent',
            field=models.BooleanField(default=True, verbose_name='\u5df2\u53d1\u9001'),
        ),
        migrations.AddField(
            model_name='task',
            name='send_time',
            field=models.DateTimeField(blank=True, help_text='\u9884\u5b9a\u53d1\u9001\u65f6\u95f4, \u9ed8\u8ba4\u9a6c\u4e0a\u53d1\u9001.', null=True, verbose_name='\u53d1\u9001\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='task',
            name='unique_id',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True, verbose_name='\u6392\u91cd'),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(blank=True, default='\u7cfb\u7edf\u6d88\u606f', max_length=32, verbose_name='\u6d88\u606f\u7c7b\u578b'),
        ),
    ]
