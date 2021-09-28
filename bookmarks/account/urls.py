from django.urls import path, include
from django.contrib.auth.views import( 
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    )
from .views import (
    dashboard,
    register,
    user_login,
    edit,
    user_list,
    user_detail,
    )

# app_name = 'account'

urlpatterns = [
    # path('login/', user_login, name='login')
    path('', dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),

    #Register
    path('register/', register, name='register'),
    #Login, logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # change password urls
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # profile edit
    path('edit/', edit, name='edit'),

    path('users/', user_list, name='user_list'),
    path('users/<username>', user_detail, name='user_detail'),

]
