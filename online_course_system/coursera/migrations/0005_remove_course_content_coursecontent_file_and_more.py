# Generated by Django 4.2.1 on 2023-07-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursera', '0004_remove_coursecontent_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='content',
        ),
        migrations.AddField(
            model_name='coursecontent',
            name='file',
            field=models.FileField(blank=True, upload_to='course_files/'),
        ),
        migrations.AddField(
            model_name='coursecontent',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
