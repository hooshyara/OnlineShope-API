from django.urls import path
from .views import Login,SignUp, LogOut,UserView

app_name = 'accounts'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('<int:id>/delete', UserView.as_view(), name='delete_user'),
    # path('search', search_cod, name='search_cod'),




    
]