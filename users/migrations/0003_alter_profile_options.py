# Generated by Django 3.2.6 on 2022-01-13 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_experience'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created']},
        ),
    ]