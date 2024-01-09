from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ContactSerializers


class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializers(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

