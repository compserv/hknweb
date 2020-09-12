# Generated by Django 2.2.8 on 2020-09-12 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0005_auto_20200910_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='recent_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='academics.Semester'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='recent_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='academics.Semester'),
        ),
        migrations.AddField(
            model_name='question',
            name='current_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='recent_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='academics.Semester'),
        ),
    ]
