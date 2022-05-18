from django.contrib import admin

from posts.models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    pass