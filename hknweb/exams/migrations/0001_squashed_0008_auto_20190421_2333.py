# Generated by Django 2.2.8 on 2022-02-28 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('exams', '0001_initial'), ('exams', '0002_auto_20180423_0200'), ('exams', '0003_auto_20180423_0534'), ('exams', '0004_auto_20180423_0536'), ('exams', '0005_auto_20180423_0544'), ('exams', '0006_auto_20190421_2245'), ('exams', '0007_auto_20190421_2314'), ('exams', '0008_auto_20190421_2333')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('release', models.BooleanField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Department')),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=255)),
                ('instructor', models.CharField(max_length=255)),
                ('midterm1', models.FileField(blank=True, upload_to='')),
                ('midterm2', models.FileField(blank=True, upload_to='')),
                ('midterm3', models.FileField(blank=True, upload_to='')),
                ('final', models.FileField(blank=True, upload_to='')),
                ('final_sol', models.FileField(blank=True, upload_to='')),
                ('midterm1_sol', models.FileField(blank=True, upload_to='')),
                ('midterm2_sol', models.FileField(blank=True, upload_to='')),
                ('midterm3_sol', models.FileField(blank=True, upload_to='')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.Course')),
            ],
        ),
    ]
