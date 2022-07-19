from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentCreateView,
    PostCommentListView,

)
from . import views
from django.urls import re_path
urlpatterns = [
    path('liked/<int:pk>/',views.like,name='post-like'),
    path('', PostListView.as_view(), name='blog-home'),
    re_path(r'^export/xls/$', views.export_post_xls, name='export_post_xls'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/comment/view/', PostCommentListView.as_view(), name='comment-view'),
    path('Import_csv/', views.Import_csv,name="Import_csv"),
]
