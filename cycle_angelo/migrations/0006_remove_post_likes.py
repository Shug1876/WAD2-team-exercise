# Generated by Django 2.2.26 on 2022-03-06 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_angelo', '0005_remove_post_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]