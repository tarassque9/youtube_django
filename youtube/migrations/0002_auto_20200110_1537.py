# Generated by Django 3.0.2 on 2020-01-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]