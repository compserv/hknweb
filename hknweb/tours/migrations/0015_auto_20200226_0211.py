# Generated by Django 2.1.11 on 2020-02-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0014_auto_20200226_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deptour',
            name='date',
            field=models.DateField(verbose_name='Desired Date'),
        ),
    ]
