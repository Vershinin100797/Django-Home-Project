import datetime

from django.contrib import admin
from django.utils import timezone

from .models import Profile, Category, Post, Comment

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comment)


def delete_old_announcement(modeladmin, request, queryset):
    queryset.filter(date_pub__lte=timezone.now() - datetime.timedelta(weeks=16)).delete()


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'announcement_image', 'announcement_title']}),
        ('Detail information', {'fields': ['description', 'category', 'price']}),
        ('Date information', {'fields': ['published_date']}),
    ]
    readonly_fields = ['published_date']
    list_display = ('author', 'announcement_title', 'published_date')
    list_filter = ('published_date', 'category')
    search_fields = ['author', 'announcement_title']
    actions = [delete_old_announcement, 'pub_now']

    @staticmethod
    def pub_now(modeladmin, request, queryset):
        queryset.update(published_date=timezone.now())


admin.site.register(Post, PostAdmin)


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


class PostInline(admin.TabularInline):
    model = Post
    fields = [
        'author',
        'announcement_image',
        'announcement_title',
        'description',
        'category',
        'price',
        'published_date'
    ]
    readonly_fields = ['published_date']
    extra = 3


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [PostInline]
