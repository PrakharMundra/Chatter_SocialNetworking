from django.urls import path
from . import views
from .views import FollowerView,FollowersView
urlpatterns = [
    path('', views.follower_name, name='user-follows'),
    path('follower/<str:user>',FollowerView.as_view(), name='follower-list'),
    path('followers/<str:user>',FollowersView.as_view(), name='followers-list')
]