from django.contrib import admin
from cycle_angelo.models import Post, Comment, UserProfile

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('content',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(UserProfile)
