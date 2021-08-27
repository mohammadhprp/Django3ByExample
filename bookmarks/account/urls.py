from django.urls import path
from django.contrib.auth.views import( 
    LoginView,
    LogoutView,
    )
from .views import (
    user_login,
    dashboard
    )

urlpatterns = [
    # path('login/', user_login, name='login')
    path('', dashboard, name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
