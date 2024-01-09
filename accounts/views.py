from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from products.models import Comment, Products
from favorite.models import Favorite
from cart.models import *
from products.forms import AddProductForm, AddCategory
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
            otp = helper.get_random_otm()
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


# def profile_view(request):
#     user_list = User.objects.all()
#     favorite = Favorite.objects.filter(user=request.user)
#     my_comment = Comment.objects.filter(user=request.user)
#     form = ProfileForm(instance=request.user)
#     add_product = AddProductForm()
#     add_blog = AddBlogForm()
#     add_category = AddCategory()
#     password_form = ChangePassword()
#     cart = Cart.objects.filter(user=request.user)
#     if request.user.is_superuser:
#         orderItem = Order.objects.all()
#         order = Order.objects.all()
#         blog = Blogs.objects.all()
#         product = Products.objects.all()
#         ticket = Tickets.objects.all().order_by('-priority')
#         contact = Contact.objects.all()
#         if request.method == 'POST':
#             print('ddd')
#             code = request.POST['search']
#             ticket = Tickets.objects.filter(code__contains=code)
#             if ticket.exists():
#                 return render(request, 'profile.html',
#                               context={'favorite': favorite, 'form': form, 'pass_form': password_form, 'cart': cart,
#                                        'comment': my_comment, 'products': product, 'add_form': add_product,
#                                        'user': user_list, 'blog': blog, 'add_blog': add_blog, 'ticket': ticket,
#                                        'contact': contact, 'add_category': add_category, 'order': order,
#                                        'orderItem': orderItem})
#             else:
#                 return render(request, 'search_not_found.html')
#         return render(request, 'profile.html',
#                       context={'favorite': favorite, 'form': form, 'pass_form': password_form, 'cart': cart,
#                                'comment': my_comment, 'products': product, 'add_form': add_product, 'user': user_list,
#                                'blog': blog, 'add_blog': add_blog, 'ticket': ticket, 'contact': contact,
#                                'add_category': add_category, 'orderItem': orderItem, 'order': order})
#     else:
#         ticket = Tickets.objects.filter(user=request.user)
#         orderItem = get_list_or_404(OrderItem, user=request.user)
#         order = get_list_or_404(Order, user=request.user)

#         print(order)
#         return render(request, 'profile.html',
#                       context={'favorite': favorite, 'form': form, 'pass_form': password_form, 'cart': cart,
#                                'comment': my_comment, 'ticket': ticket, 'orderItem': orderItem, 'order': order})


# def updat_profile(requset):
#     user = get_object_or_404(User, id=requset.user.id)
#     form = ProfileForm(requset.POST, requset.FILES, instance=user)

#     if form.is_valid():

#         form.save()
#         return redirect(reverse('accounts:profile_view'))
#     else:
#         print(form.errors)
#     return redirect(reverse('accounts:profile_view'))


# def change_password(request):
#     user = get_object_or_404(User, id=request.user.id)
#     form = ChangePassword(request.POST)
#     if form.data['password1'] == form.data['password2']:
#         user.password = make_password(form.data['password1'])
#         user.save()
#         return redirect(reverse('Home:HomeView'))

#     return redirect(reverse('accounts:profile_view'))


# def user_detail(request, pk):
#     if request.user.is_superuser:
#         user = get_object_or_404(User, id=pk)
#         form = ProfileForm(instance=user)
#         if request.method == "POST":
#             form = ProfileForm(request.POST, request.FILES, instance=user)

#             if form.is_valid():
#                 print('dd')

#                 form.save()
#                 return redirect(reverse('accounts:profile_view'))
#             else:
#                 print(form.errors)

#         return render(request, 'account_cart.html', context={'UPform': form, 'user': user})


class UserView(APIView):
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        if user.is_superuser:
            target_user = User.objects.get(id=id)
            target_user.delete()
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
