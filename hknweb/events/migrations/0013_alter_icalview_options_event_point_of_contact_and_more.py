# Generated by Django 4.2.5 on 2024-10-26 00:05

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0012_icalview"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="icalview",
            options={"verbose_name": "iCal view"},
        ),
        migrations.AddField(
            model_name="event",
            name="point_of_contact",
            field=models.CharField(default="N/A", max_length=255),
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=markdownx.models.MarkdownxField(max_length=2000),
        ),
    ]
