from rest_framework import serializers
from .models import Tickets, TicketMessage



class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ['title', 'user', 'date', 'active', 'code', 'priority', 'status']
        

class TicketMessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ['ticket', 'user', 'message', 'file', 'date',  ]
        

