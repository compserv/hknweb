# Generated by Django 2.2.8 on 2021-02-02 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesemester', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='year',
            field=models.IntegerField(default=2020),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester',
            field=models.CharField(max_length=10),
        ),
    ]
