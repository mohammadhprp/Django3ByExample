from django import template
from django.db.models import Count
from ..models import Post 

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_lastes_posts(count=5):
  lastes_posts = Post.published.order_by('-publish')[:count]
  return {'lastes_posts' : lastes_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
  return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]