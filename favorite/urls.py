from django.urls import path
from .views import  FavoriteView

app_name = 'favorite'


urlpatterns = [
    path('wishlist', FavoriteView.as_view(), name='wishlist'),
    path('<int:id>/wishlist', FavoriteView.as_view(), name='add_to_favorite'),
    




] 
