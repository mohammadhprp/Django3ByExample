from django.urls import path
from .feeds import LatestPostsFeed

from .views import (
    post_list,
    post_detail,
    PostListView,
    post_share,
  )


app_name = 'blog'

urlpatterns = [
  path('', post_list, name='post_list'),
  # path('', PostListView.as_view(), name='post_list' ),
  path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
  path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        post_detail, name='post_detail'
    ),
  path('<int:post_id>/share/', post_share, name='post_share'),
  path('feed/', LatestPostsFeed(), name='post_feed'),
]
