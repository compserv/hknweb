# Generated by Django 2.1.11 on 2019-11-27 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dept_tours', '0002_auto_20191125_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departmenttourrequest',
            name='email2',
        ),
    ]
