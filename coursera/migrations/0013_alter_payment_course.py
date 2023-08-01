# Generated by Django 4.2.1 on 2023-07-21 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursera', '0012_rename_course_id_payment_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='coursera.course'),
        ),
    ]
