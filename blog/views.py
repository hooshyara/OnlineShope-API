from django.shortcuts import reverse, get_object_or_404
from .models import Blogs, Comments
from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BlogSerializers, CommentSerializers
from accounts.helper import get_user


class BlogListView(APIView):
    def get(self, request, id=None):
        if id:
            blog = Blogs.objects.get(id=id)
            serializer = BlogSerializers(blog, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = User()
            blog_list = Blogs.objects.filter(is_active=True)
            serializer = BlogSerializers(blog_list, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.data.get("token")
        user = get_user(token)
        if user.is_superuser:
            serializer = BlogSerializers(data=request.data)
            if serializer.is_valid():
                blog = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            blog = Blogs.objects.get(id=id)
            blog_id = blog.id
            blog.delete()
            return Response({"message": f"blog{blog_id} is delete"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "blog is not exist"})

    def put(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        serializer = BlogSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)


class CommentsView(APIView):
    def get(self, request, id):
        blog = Blogs.objects.get(id=id)
        comment = Comments.objects.filter(blog=blog)
        serializer = CommentSerializers(comment, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        blog = Blogs.objects.get(id=id)
        comment = Comments.objects.create(
            blog=blog,
            user=user,
            star=request.data.get('star'),
            text=request.data.get('text')
        )
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        if user.is_superuser:
            comment = Comments.objects.get(id=id)

            comment.delete()
            return Response({"message": " comment is delete"}, status=status.HTTP_400_BAD_REQUEST)







