# Generated by Django 2.1.11 on 2019-11-26 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentTourRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=85)),
                ('tour_date', models.DateTimeField()),
                ('email_address', models.EmailField(max_length=85)),
                ('retype_email_address', models.EmailField(max_length=85)),
                ('phone_number', models.CharField(default='', max_length=12)),
                ('comments', models.TextField(blank=True, default='', max_length=2000)),
            ],
        ),
    ]
