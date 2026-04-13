from django.contrib import admin
from django.urls import include,path
from . import views
from django.contrib.auth import views as auth_views
app_name='users'
urlpatterns = [
    path('auth/',views.auth,name='auth'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='users:login'),name='logout'),
    path('profile/',views.profile,name='profile'),
    path('profile/<int:id>/',views.seller_profile,name='profile_with_id'),
    path('createprofile/<int:user_id>',views.CreateProfile,name='create_profile')
]