from django.contrib import admin

from posts.models import User

# Register your models here.

@admin.register(User)
class PostModelAdmin(admin.ModelAdmin):
    pass