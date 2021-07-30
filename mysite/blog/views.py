from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
  posts = Post.published.all()
  context = {
    'posts': posts,
  }
  return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post, slug=post,
                        status='published',
                        publish__year=year,
                        publish__month=month,
                        publish__day=day)
  context = {
    'post': post,
  }

  return render(request, 'blog/post/detail.html', context)
