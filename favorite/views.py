from django.shortcuts import render ,redirect, get_object_or_404, reverse
from .models import Favorite
from products.models import Products
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.helper import get_user
from .serializers import FavoriteSerializers

class FavoriteView(APIView):
    def get(self, request):
        token = request.data.get("token")
        user = get_user(token)
        favorite = Favorite.objects.filter(user=user)
        serializers = FavoriteSerializers(favorite, many=True, context={"request":request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        print(user)
        product = Products.objects.get(id=id)
        print(product)
        favorite = Favorite.objects.create(
            user = user,
            product=product,
        )
        favorite.save()
        
        
        return Response({"message":"ok"}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        if user:
            favorite = Favorite.objects.get(id=id)
            favorite.delete()
            return Response({"message":"ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"User in Invalid"}, status=status.HTTP_404_NOT_FOUND)






def favorite_items(request):
    favorite = Favorite.objects.filter(user=request.user)

    return render(request, 'wish_list.html', context={'favorite':favorite})




