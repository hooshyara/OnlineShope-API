from django.shortcuts import render, redirect, get_object_or_404
from products.models import Products
from .models import Cart, Order, OrderItem
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.helper import get_user
from .serializers import CartSerializers, OrderSerializers
from rest_framework.response import Response


class CartView(APIView):
    def post(self, request, id=None):
        token = request.data.get("token")
        user = get_user(token)
        if id:
            product = Products.objects.get(id=id)
            if Cart.objects.filter(user=user, products=product).exists():
                cart = Cart.objects.get(user=user, products=product)
                cart.count = int(cart.count) + int(request.data.get('product_count'))
                cart.save()
                cart.end_price = str(cart.count * product.second_price)
                cart.save()
            else:
                print(user)
                count = request.data.get('product_count')              
                cart = Cart.objects.create(
                    user=user, 
                    products=product,
                    count = count,
                    end_price = str(product.second_price * int(count)), 
                )
                cart.save()
            return Response({"message":"ok"}, status=status.HTTP_200_OK)
        else:
            
            token = request.data.get("token")
            user = get_user(token)
            print("mmmmmmmmmmmmmmmmmuser")
            cart = Cart.objects.filter(user=user)
            serializers = CartSerializers(cart, many=True, context={"request":request})
            return Response(serializers.data, status=status.HTTP_200_OK)
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        product = Products.objects.get(id=id)
        cart = get_object_or_404(Cart, products=product, user=user)
        cart.delete()
        return Response({"message":"ok"}, status=status.HTTP_200_OK)


class CheckOut(APIView):
    def post(self, request):
        token = request.data.get("token")
        user = get_user(token)
        print(user)
        cart = Cart.objects.filter(user=user)
        
        total_price = 0
        for i in cart:
            total_price = total_price + i.products.second_price * i.count
        order = Order.objects.create(
            user = user,
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            city = request.data.get('city'),
            # description = form.data['description'],
            post_id = request.data.get('post_id'),
            totla_price = total_price
        )
        order.save()
        for item in cart:
            product = Products.objects.get(id=item.products.id)
            orderItem = OrderItem.objects.create(
                user = user,
                order = order,
                product = product,
                product_price = item.products.price,
                product_count = item.count,
                product_cost = item.end_price

            )
            orderItem.save()
            product.inventory -= item.count
            product.save()
            product_cart = Cart.objects.get(user=user, products=product)
            product_cart.delete()
        return Response({"message":"ok"}, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        print(user.is_superuser)
        if user.is_superuser or user.is_shope:
            order = Order.objects.get(id=id)
            serializer = OrderSerializers(order,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            
