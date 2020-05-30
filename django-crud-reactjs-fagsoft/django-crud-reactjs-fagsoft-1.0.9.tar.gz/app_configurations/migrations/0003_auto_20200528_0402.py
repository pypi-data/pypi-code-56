# Generated by Django 3.0.6 on 2020-05-28 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_configurations', '0002_auto_20200411_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinfoconfiguration',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='generalinfoconfiguration',
            name='application_name',
            field=models.CharField(default='App. Name', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalinfoconfiguration',
            name='contact_emails',
            field=models.TextField(blank=True, null=True),
        ),
    ]
