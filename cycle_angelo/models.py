from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Post(models.Model):

    post_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='blog_post_images', blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):

        return self.content

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=150)

    def __str__(self):
        return self.content
        
#class UserProfile(models.Model):
 #   user = models.OneToOneField(User, on_delete=models.CASCADE)
    
  #  user_ID = models.AutoField(primary_key=True)
   # username = models.CharField(unique=True, max_length=100)
    #user_type = models.CharField(max_length=100)
    #picture = models.ImageField(upload_to='profile_images', blank=True)





