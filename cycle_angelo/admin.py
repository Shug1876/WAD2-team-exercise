from django.contrib import admin
from cycle_angelo.models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('content',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
