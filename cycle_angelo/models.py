from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)


    def __str__(self):
        return self.user.username

class Post(models.Model):
    TITLE_MAX_LENGTH = 128
    post_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='blog_post_images', blank=True)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):

        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=150)

    def __str__(self):
        return self.content
        






