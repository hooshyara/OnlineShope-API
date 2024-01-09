from django.contrib import admin
from .models import Blogs, Comments, Reply



@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'datetime_created', 'id']




@admin.register(Blogs)
class BlogAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'datetime_created', 'id']




