from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# Show all models
# admin.site.register(Post)

# Customizing model display

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'author', 'publish', 'status')
  list_filter = ('title', 'created', 'publish', 'author')
  search_fields = ('title', 'body')
  prepopulated_fields = {'slug': ('title', )}
  raw_id_fields = ('author',)
  date_hierarchy = 'publish'
  ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'post', 'created', 'active')
  list_filter = ('active', 'created', 'updated')
  search_fields = ('name', 'email', 'body')
