# Generated by Django 2.2.8 on 2022-03-07 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_attendanceresponse_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceform',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]