from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm

# Create your views here.

# using class-base views
class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 2
  template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
  object_list = Post.published.all()
  tag = None

  if tag_slug:
      tag = get_object_or_404(Tag, slug=tag_slug)
      object_list = object_list.filter(tags__in=[tag])

  paginator = Paginator(object_list, 3) # 3 posts in each page
  page = request.GET.get('page')
  try:
      posts = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer deliver the first page
      posts = paginator.page(1)
  except EmptyPage:
      # If page is out of range deliver last page of results
      posts = paginator.page(paginator.num_pages)

  context = {
    'page': page,
    'posts': posts,
    'tag': tag
    }

  return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post, slug=post,
                        status='published',
                        publish__year=year,
                        publish__month=month,
                        publish__day=day)

  comments = post.comments.filter(active=True)

  new_comment = None 

  if request.method == 'POST':
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.post = post
      new_comment.save()
  else:
    comment_form = CommentForm()

  post_tags_ids = post.tags.values_list('id', flat=True)
  similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
  similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]




  context = {
    'post': post,
    'comments': comments,
    'new_comment': new_comment,
    'comment_form': comment_form,
    'similar_posts': similar_posts
  }

  return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
  post = get_object_or_404(Post,  id=post_id, status='published')
  sent = False

  if request.method == 'POST':
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = f"{cd['name']} recommends you read {post.title}"
      message = f"Read {post.title} at {post_url} \n\n {cd['name']}\'s comments: {cd['comments']}"
      send_mail(subject, message, 'youremail@gmail.com', [cd['to']])
      sent = True
  else:
    form = EmailPostForm()

  context = {
    'post': post,
    'form': form,
    'sent': sent
  }
  return render(request, 'blog/post/share.html', context)


def post_search(request):
  form = SearchForm()
  query = None
  results = []
  if 'query' in request.GET:
    form = SearchForm(request.GET)
    if form.is_valid():
      query = form.cleaned_data['query']
      # search_vectoor = SearchVector('title', weight='A') + SearchVector('body', weight='B')
      # search_query = SearchQuery(query)
      results = Post.published.annotate(
        similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')

  context = {
    'form': form,
    'query': query,
    'results': results,
  }

  return render(request, 'blog/post/search.html', context)
