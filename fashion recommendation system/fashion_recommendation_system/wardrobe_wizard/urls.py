from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("user_signup", views.user_signup, name="user_signup"),
    path("user_login", views.user_login, name="user_login"),
    path('user_logout', views.user_logout, name='user_logout'),
    path('upload_upper', views.upload_upper, name='upload_upper'),
    path('delete_upper/<int:pk>/', views.delete_upper, name='delete_upper'),
    path('upload_lower', views.upload_lower, name='upload_lower'),
    path('delete_lower/<int:pk>/', views.delete_lower, name='delete_lower'),
    path('match_clothes_view', views.match_clothes_view, name='match_clothes_view'),
]