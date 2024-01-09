from django.shortcuts import render, redirect, reverse
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import TicketSerializers, TicketMessageSerializers
from accounts.helper import get_user



class TicketView(APIView):
    def post(self, request, id=None):
        if id:
            token = request.data.get("token")
            user = get_user(token)
            print(id)
            ticket = Tickets.objects.get(id=id)
            print(ticket.user)
            ticket_message = TicketMessage.objects.create(
                ticket=ticket,
                user=user,
                message=request.data.get('message'),
                file = request.data.get('file')
                
            )
            ticket_message.save()
            return Response({"message":"ok"}, status=status.HTTP_200_OK)
        else:
            token = request.data.get("token")
            user = get_user(token)
            # serializers = TicketSerializers(data=request.data)
            # if serializers.is_valid():
            #     ticket = serializers.save()
            #     return Response(serializers.data, status=status.HTTP_200_OK)
            ticket = Tickets.objects.create(
                user=user,
                title=request.data.get('title'),
                priority=request.data.get('priority'),
                status=request.data.get('status'),
                active=request.data.get('active')
            )
            ticket.save()
            return Response({"message":"ok"}, status=status.HTTP_200_OK)
    def delete(self, request, id):
        token = request.data.get("token")
        user = get_user(token)
        if user.is_superuser:
            ticket = Tickets.objects.get(id=id)
            ticket.delete()
            return Response({"message":"ok"}, status=status.HTTP_200_OK)







