# Generated by Django 2.2.8 on 2020-09-10 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_auto_20200901_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='current_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='current_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='current_first_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='current_instructor_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='current_last_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]