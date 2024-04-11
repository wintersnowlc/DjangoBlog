from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Article


class IndexView(ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(publish_at__lte=timezone.now())


class ArticleView(DetailView):
    model = Article


class CategoryView(ListView):
    model = Article
    template_name = 'blog/article_list.html'

    def get_queryset(self):
        return Article.objects.filter(publish_at__lte=timezone.now(), category=self.kwargs['pk'])


class TagView(ListView):
    model = Article
    template_name = 'blog/article_list.html'

    def get_queryset(self):
        return Article.objects.filter(publish_at__lte=timezone.now(), tags=self.kwargs['pk'])
