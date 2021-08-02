from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post

# Create your views here.

# using class-base views
class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 2
  template_name = 'blog/post/list.html'


def post_list(request):
  object_list = Post.published.all()
  paginator = Paginator(object_list, 3) # 3 posts in each page
  page = request.GET.get('page')

  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # if page not an integer deliver the first page
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  context = {
    'page': page,
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


