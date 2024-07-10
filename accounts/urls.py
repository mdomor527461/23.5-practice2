from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name = 'register'),
    path('login/',views.UserLoginView.as_view(),name = 'login'),
    path('logout/',views.user_logout,name = 'logout'),
    path('profile/',views.UserUpdateView.as_view(),name = 'profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/passchange.html'), name='passchange'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]