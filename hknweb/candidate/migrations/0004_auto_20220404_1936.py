# Generated by Django 2.2.8 on 2022-04-05 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_auto_20220330_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementmandatory',
            name='events',
            field=models.ManyToManyField(blank=True, to='events.Event'),
        ),
    ]
