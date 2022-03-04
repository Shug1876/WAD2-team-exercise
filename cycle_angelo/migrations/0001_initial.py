# Generated by Django 2.2.26 on 2022-03-03 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_ID', models.IntegerField(unique=True)),
                ('content', models.CharField(max_length=200)),
                ('likes', models.IntegerField(default=0)),
                ('picture', models.ImageField(blank=True, upload_to='blog_post_images')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_ID', models.IntegerField(unique=True)),
                ('content', models.CharField(max_length=100)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycle_angelo.BlogPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycle_angelo.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycle_angelo.UserProfile'),
        ),
    ]