from django.contrib import admin
from apps.blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "modified")
    list_per_page = 20


admin.site.register(Post, PostAdmin)
