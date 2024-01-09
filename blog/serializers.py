from rest_framework import serializers
from .models import Blogs, Comments



class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['title', 'user', 'content', 'cover', 'datetime_created', 'datetime_modified', 'is_active', ]
        

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['blog', 'user', 'star', 'datetime_created', 'datetime_modified',  'text']

        