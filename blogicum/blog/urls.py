from django.urls import path, include

from . import views


app_name = 'blog'

posts_patterns = [
    path('<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('create/', views.PostCreateView.as_view(),
         name='create_post'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
]

comment_patterns = [
    path('comment/',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('edit_comment/<int:comment_pk>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('delete_comment/<int:comment_pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
]

profile_patterns = [
    path('edit_profile/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('<str:slug>/',
         views.ProfileDetailView.as_view(), name='profile'),
]
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/', include(posts_patterns)),
    path('posts/<int:pk>/', include(comment_patterns)),
    path('profile/', include(profile_patterns)),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),
]
