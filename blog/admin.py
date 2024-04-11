from django.contrib import admin
from django.utils import timezone
from django.db.models import Q

from .models import Author, Tag, Category, Article, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'user', 'signature')
    search_fields = ('nickname', 'user__username')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


# 文章是否发布过滤
class PublishedListFilter(admin.SimpleListFilter):
    title = '发布状态'
    parameter_name = 'publish_at'

    def lookups(self, request, model_admin):
        return (
            ('published', '已发布'),
            ('draft', '草稿')
        )

    def queryset(self, request, queryset):
        if self.value() == 'published':
            # 存在发布时间且早于当前时间的文章
            return queryset.filter(published_at__lt=timezone.now())
        if self.value() == 'draft':
            # 不存在发布时间或发布时间晚于当前时间的文章
            cond = Q(published_at__gte=timezone.now()) | Q(published_at__isnull=True)
            return queryset.filter(cond)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish_at', 'read_count')
    search_fields = ('title', 'author__nickname', 'category__name')
    list_filter = ('category', 'tags', PublishedListFilter)
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'summary', 'body')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('publish_at', 'author', 'tags')
        })
    )

    def get_changeform_initial_data(self, request):
        return {'author': Author.objects.get(user=request.user)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', '__str__')
