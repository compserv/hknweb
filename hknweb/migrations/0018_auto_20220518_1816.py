# Generated by Django 2.2.8 on 2022-05-19 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hknweb', '0017_auto_20220518_1813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='committeeship',
            old_name='elections',
            new_name='election',
        ),
    ]
