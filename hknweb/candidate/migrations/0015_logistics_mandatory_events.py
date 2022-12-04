# Generated by Django 2.2.28 on 2022-12-03 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_eventphoto'),
        ('candidate', '0014_externalreq_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='logistics',
            name='mandatory_events',
            field=models.ManyToManyField(blank=True, to='events.Event'),
        ),
    ]
