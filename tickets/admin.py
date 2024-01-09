from django.contrib import admin
from .models import Tickets, TicketMessage

@admin.register(Tickets)
class TicketAdmin(admin.ModelAdmin):
    list_display   = [ 'title', 'status', 'id']





@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display   = [ 'user']