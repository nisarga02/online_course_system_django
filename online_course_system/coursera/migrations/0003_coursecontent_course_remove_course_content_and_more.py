# Generated by Django 4.2.1 on 2023-07-15 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursera', '0002_course_coursecontent_purchase_course_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecontent',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='coursera.course'),
        ),
        migrations.RemoveField(
            model_name='course',
            name='content',
        ),
        migrations.AddField(
            model_name='course',
            name='content',
            field=models.ManyToManyField(blank=True, related_name='contents', to='coursera.coursecontent'),
        ),
    ]
