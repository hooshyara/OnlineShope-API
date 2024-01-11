from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from .models import Products, Comment, Category, Comparison
from django.views import generic
from .forms import CommentForm, AddProductForm, AddCategory
from django.core.paginator import Paginator
from .filters import ProductFilter
from .serializers import ProductSerializers, ComparisonSerializers, CommentSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.helper import get_user



class ProductListView(APIView):
    def get(self, request):
        q = request.GET.get('q')
        if q:
            product = Products.objects.filter(Category__name=q)
        else:
            product = Products.objects.all()
        user = User()
        serializers = ProductSerializers(product, many=True, context={'request':request})
        return Response(serializers.data, status=status.HTTP_200_OK)
    def post(self, request):
        token = request.data.get("token")
        user = get_user(token)
        category = Category.objects.get(name=request.data.get('category'))
        print(f'user:{user}')
        if user.is_superuser:
            product = Products.objects.create(
                user=user,
                title=request.data.get('title'),
                content=request.data.get('content'),
                cover = request.data.get('cover'),
                star = request.data.get('star'),
                price = request.data.get('price'),
                inventory = request.data.get('inventory'),
                active = request.data.get('active'),
                discouont = request.data.get('discouont'),
                category=category

            )
            product.save()
        return Response({"message":"OK"}, status=status.HTTP_200_OK)

    def put(self, request, id):
        token = request.data.get("token")        
        user = get_user(token)        
        product = Products.objects.get(id=id)
        if user.is_superuser:
            serializer = ProductSerializers(product,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(f'user:{user}')
    
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        product = Products.objects.get(id=id)
        if user.is_superuser:
            product.delete()
            return Response({"message":"product is delete"}, status=status.HTTP_200_OK)


        


class ComparisonView(APIView):
    def get(self, request):
        token = request.data.get("token")
        user = get_user(token)
        favorite = Comparison.objects.filter(user=user)
        serializers = ComparisonSerializers(favorite, many=True, context={"request":request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        print(user)
        product = Products.objects.get(id=id)
        print(product)
        favorite = Comparison.objects.create(
            user = user,
            product=product,
        )
        favorite.save()
        return Response({"message":"ok"}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        comparison = Comparison.objects.get(id=id)
        comparison.delete()
        return Response({"message":"ok"}, status=status.HTTP_200_OK)

        



class CommentsView(APIView):
    def get(self, request, id):
        blog = Products.objects.get(id=id)
        comment = Comment.objects.filter(blog=blog)
        serializer = CommentSerializers(comment, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        blog = Products.objects.get(id=id)
        comment = Comment.objects.create(
            product=blog,
            user=user,
            star=request.data.get('star'),
            text=request.data.get('text')
        )
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        if user.is_superuser:
            comment = Comment.objects.get(id=id)

            comment.delete()
            return Response({"message": " comment is delete"}, status=status.HTTP_400_BAD_REQUEST)

