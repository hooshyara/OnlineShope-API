from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from .models import Products, Comment, Category
from django.views import generic
from .forms import CommentForm, AddProductForm, AddCategory
from django.core.paginator import Paginator
from .filters import ProductFilter
from .serializers import ProductSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.helper import get_user



class ProductListView(APIView):
    def get(self, request):
        user = User()
        product = Products.objects.all()
        serializers = ProductSerializers(product, many=True, context={'request':request})
        return Response(serializers.data, status=status.HTTP_200_OK)
    def post(self, request):
        token = request.data.get("token")
        user = get_user(token)
        print(f'user:{user}')
        if user.is_superuser:
            serializer = ProductSerializers(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


        



   



def search_product(request):
    if request.method == "POST":
        title = request.POST['search']
        product = Products.objects.filter(title__contains=title)
        if product.exists():

            return render(request, 'product_list.html', context={'page_obj': product})
        else:
            return render(request, 'search_not_found.html')






