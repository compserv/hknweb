# Generated by Django 2.2.8 on 2021-12-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True, max_length=1000)),
                ('document', models.FileField(upload_to='resume/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('critiques', models.TextField(blank=True, max_length=10000)),
            ],
        ),
    ]
