# Generated by Django 2.2.8 on 2022-02-28 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hknweb', '0016_profile_google_calendar_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='candidate_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coursesemester.Semester'),
        ),
    ]
