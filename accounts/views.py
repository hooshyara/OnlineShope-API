from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from products.models import Comment, Products, Category
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializers
from cart.models import *
from products.serializers import ProductSerializers
from blog.models import Blogs
from tickets.models import Tickets, TicketMessage
from contact.models import Contact
from . import helper
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .jwt_utils import generate_jwt_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.helper import get_user
from .serializers import UserSerializers
from contact.serializers import ContactSerializers
from tickets.serializers import TicketSerializers
from cart.serializers import OrderSerializers, OrderItemSerializers
from blog.serializers import BlogSerializers
from products.serializers import CommentSerializers


class Login(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        user = User.objects.get(mobile=mobile)

        if user.check_password(password):
            accessToken, refresh_tocken = generate_jwt_token(user)
            return Response({
                'access_token': accessToken,
                'refresh_tocken': refresh_tocken,
            })
        else:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        if mobile and password:
            user = User.objects.create_user(mobile=mobile, password=password)
            otp = helper.get_random_otp()
            helper.send_otp(mobile, otp)
            user.otp = otp
            user.is_active = False
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)


class LogOut(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_tocken = request.data.get('refresh_tocken')
        print(refresh_tocken)
        token = RefreshToken(refresh_tocken)
        token.blacklist()
        return Response({"message": "user is LogOut"}, status=status.HTTP_205_RESET_CONTENT)



class ProfileView(APIView):
    def post(self, request):
        token = request.data.get("token")
        user = get_user(token)
        favorite = Favorite.objects.filter(user=user)
        favorite_serializers = FavoriteSerializers(favorite, many=True, context={"request":request})
        cart = Cart.objects.filter(user=user)
        if user.is_superuser:
            orderItem = Order.objects.all()
            orderItem_serializers = OrderItemSerializers(orderItem, many=True, context={"request":request})
            order = Order.objects.all()
            order_serializers = OrderSerializers(order, many=True, context={"request":request})
            blog = Blogs.objects.all()
            blog_serializers = BlogSerializers(blog, many=True, context={"request":request})
            product = Products.objects.all()
            product_serializers = ProductSerializers(product, many=True, context={"request":request})
            ticket = Tickets.objects.all()
            ticket_serializers = ProductSerializers(ticket, many=True, context={"request":request})
            contact = Contact.objects.all()
            contact_serializers = ContactSerializers(contact, many=True, context={"request":request})
            return Response({"products":product_serializers.data, "orderItems":orderItem_serializers.data, 
                             "orders":order_serializers.data, "blogs":blog_serializers.data, "tickets":ticket_serializers.data, 
                             "contact":contact_serializers.data, "favorite":favorite_serializers.data}, status=status.HTTP_200_OK)
        else:
            print(user)
            if user.is_shope:
                category = Category.objects.get(name=request.data.get('category'))
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
                category=category,
                percent = request.data.get('percent')

            )
                product.save()
                comment = Comment.objects.filter(product__user=user)
                comment_serializers = CommentSerializers(comment, many=True, contex={"request":request})
                return Response(comment_serializers.data, {"message":"OK"}, status=status.HTTP_200_OK)
            else:
                ticket = Tickets.objects.filter(user=user)
                ticket_serializers = ProductSerializers(ticket, many=True, context={"request":request})
                orderItem = OrderItem.objects.filter(user=user)
                orderItem_serializers = OrderItemSerializers(orderItem, many=True, context={"request":request})
                order = Order.objects.filter(user=user)
                order_serializers = OrderSerializers(order, many=True, context={"request":request})
                return Response({ "orderItems":orderItem_serializers.data, 
                                "orders":order_serializers.data,  "tickets":ticket_serializers.data, 
                                "favorite":favorite_serializers.data}, status=status.HTTP_200_OK)
    def put(self, request):
        token = request.data.get("token")
        user = get_user(token)
        serializers = UserSerializers(user, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




class ChangePaasword(APIView):
    def post(self, request):
            token = request.data.get("token")
            user = get_user(token)
            user.password = make_password(request.data.get('password'))
            user.save()
            return Response({"message":"your password was Changed"}, status=status.HTTP_200_OK)

            

class UserView(APIView):
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        if user.is_superuser:
            target_user = User.objects.get(id=id)
            target_user.delete()
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
