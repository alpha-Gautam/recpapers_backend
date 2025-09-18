

# Routers provide an easy way of automatically determining the URL conf.
from django.contrib import admin
from django.urls import include, path
from .views import RegistrationView, LoginView,GetCookies, ActivateView, UserDetailsView, ForgotPasswordView, ResetPasswordPageView, UpdatePasswordView, LogoutView, DeleteUserView


from django.http import HttpResponse

urlpatterns = [
    path('get-cookies/', GetCookies.as_view(), name='get-cookies'),
    
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<str:uid>/<str:token>/', ResetPasswordPageView.as_view(), name='reset_password'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
    path('logout/', LogoutView.as_view(), name='logout'),

]

