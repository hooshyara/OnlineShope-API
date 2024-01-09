from django.urls import path
from .views import  TicketView



app_name = 'ticket'
urlpatterns = [
    path('', TicketView.as_view(), name='ticket'),
    path('<int:id>', TicketView.as_view(), name='ticket_detail'),
    path('<int:id>/delete', TicketView.as_view(), name='ticket_delete'),

    


    
]
