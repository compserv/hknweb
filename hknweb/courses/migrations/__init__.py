

from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                # ('id', models.IntegerField(primary_key=True, serialize=False)),
                # ('name', models.CharField(max_length=255)),
                # ('slug', models.CharField(max_length=255)),
                # ('location', models.CharField(max_length=255)),
                # ('description', models.TextField()),
                # ('start_time', models.DateTimeField()),
                # ('end_time', models.DateTimeField()),
                # ('event_type_id', models.IntegerField()),
                # ('need_transportation', models.BooleanField(default=False)),
                # ('markdown', models.BooleanField(default=False)),
                # ('created_at', models.DateTimeField(auto_now_add=True)),
                # ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, null=False)),
				('description', models.TextField()),
				('Prerequisites', models.TextField()),
				('Wordload', models.TextField()),
				('TopicCovered', models.TextField()),
            ],
        ),
       
    ]
