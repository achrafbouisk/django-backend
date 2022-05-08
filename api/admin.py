from django.contrib import admin

from .models import Post
from .models import Category 
from .models import User
from .models import Comment
from .models import Reply


# Register your models here.
admin.site.site_header = "My back-office"
admin.site.site_title = "Admin pannel"
# admin.site.index_title = "Welcome to Portal"
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'date_added', 'last_modified', 'is_draft') #data table
    search_fields = ('title',) #search bar
    list_filter = ('is_draft','date_added', 'category') #i want filter data by category
    prepopulated_fields = {'slug': ('title', )} #slug's value = title + -
    list_pre_page = 100  #the max of line selected
    actions = ('set_posts_to_published', 'set_posts_not_to_published') #list of actions 
    fields = (('title', 'slug','category'),'description', ('image', 'is_draft') )

    def set_posts_to_published(self, request, queryset):
        count = queryset.update(is_draft=True)
        self.message_user(request, '{} post has been published successfully.'.format(count))
    set_posts_to_published.short_description = 'Mark selected posts as published'

    def set_posts_not_to_published(self, request, queryset):
        count = queryset.update(is_draft=False )
        self.message_user(request, '{} post hasnt been published successfully.'.format(count))
    set_posts_not_to_published.short_description = 'Mark selected posts to not published'

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'body')
    search_fields = ('body',)
    
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'body')
    search_fields = ('body',)

admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)

