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


# urlpatterns = [
#     path('', views.PostListView.as_view(), name='index'),
#     path('posts/<int:pk>/', views.PostDetailView.as_view(),
#          name='post_detail'),
#     path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(),
#          name='edit_post'),
#     path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(),
#          name='delete_post'),
#     path('posts/<int:pk>/comment/',
#          views.CommentCreateView.as_view(), name='add_comment'),
#     path('posts/<int:pk>/edit_comment/<int:comment_pk>/',
#          views.CommentUpdateView.as_view(), name='edit_comment'),
#     path('posts/<int:pk>/delete_comment/<int:comment_pk>/',
#          views.CommentDeleteView.as_view(), name='delete_comment'),
#     path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
#          name='category_posts'),
#     path('posts/create/', views.PostCreateView.as_view(),
#          name='create_post'),
#     path('profile/edit_profile/',
#          views.ProfileUpdateView.as_view(), name='edit_profile'),
#     path('profile/<str:slug>/',
#          views.ProfileDetailView.as_view(), name='profile'),
# ]
