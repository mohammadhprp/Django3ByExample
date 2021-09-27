from django.urls import path
from .views import (
    image_create,
    image_detail,
    image_like,
    image_list
  )

app_name='images'

urlpatterns = [
  path('', image_list, name='list'),
  path('create/', image_create, name='create'),
  path('detail/<int:id>/<slug:slug>/', image_detail, name='detail'),
  path('like/', image_like, name='like')
]
