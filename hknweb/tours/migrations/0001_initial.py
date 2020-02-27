# Generated by Django 2.1.11 on 2020-02-10 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepTour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=255)),
                ('desired_date', models.DateTimeField()),
                ('phone', models.CharField(default='', max_length=12)),
                ('comments', models.TextField(blank=True, default='', max_length=2000, verbose_name='Additional comments')),
                ('reviewed', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Department Tours',
            },
        ),
    ]
