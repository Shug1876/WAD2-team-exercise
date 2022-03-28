import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Attributes
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    TITLE_MAX_LENGTH = 128
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    creator = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='posts',
        editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    number_of_comments = models.IntegerField(default=0)

    title = models.CharField(max_length=TITLE_MAX_LENGTH, default="[No post title]")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'posts'
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_ID = models.AutoField(primary_key=True)
    content = models.TextField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
