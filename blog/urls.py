from django.urls import path
from .views import BlogListView,  CommentsView
app_name = 'blog'
urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('/<int:id>', BlogListView.as_view(), name='blog_detail'),
    path('/<int:id>/comment/', CommentsView.as_view(), name='comment_create'),
    path('/<int:id>/comment/delete', CommentsView.as_view(), name='comment_delete'),
    path('/<int:id>/delete/', BlogListView.as_view(), name='delete_blog'),



]