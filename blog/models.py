import re
import uuid

from django.db import models as m
from django.contrib.auth.models import User
from django.utils.text import slugify

# noinspection PyPackageRequirements
from mdeditor.fields import MDTextField


class Author(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE, verbose_name='用户')
    nickname = m.CharField(max_length=20, blank=True, verbose_name='昵称')
    signature = m.CharField(max_length=100, null=True, blank=True, verbose_name='签名')
    avatar = m.ImageField(upload_to='blog/avatars/', null=True, blank=True, verbose_name='头像')

    def __str__(self):
        return self.nickname  # Returns author's nickname when the object is printed.

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.nickname:
            self.nickname = self.user.username
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name


class Tag(m.Model):
    name = m.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Category(m.Model):
    name = m.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Article(m.Model):
    title = m.CharField(max_length=100, unique=True)
    slug = m.SlugField(max_length=32, unique=True, blank=True)
    summary = m.CharField(max_length=200, null=True, blank=True)
    body = MDTextField()
    create_at = m.DateTimeField(auto_now_add=True)
    update_at = m.DateTimeField(auto_now=True)
    publish_at = m.DateTimeField(null=True, blank=True)
    read_count = m.PositiveIntegerField(default=0, editable=False)

    author = m.ForeignKey(Author, on_delete=m.CASCADE)
    category = m.ForeignKey(Category, on_delete=m.CASCADE)
    tags = m.ManyToManyField(Tag, blank=True)

    # Custom save method to add slug.
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            while (not slug) or Article.objects.filter(slug=slug).exists():
                slug = slug + '-' + str(uuid.uuid4())[:8]
            self.slug = slug
        # 逐行检查是否存在标题行内容前存在空格的情况，如果存在则去掉，因为markdown解析时无法识别空格开头的标题
        lines = self.body.split('\n')
        re_title = re.compile(r'^\s*#+\s+\S')
        for i, line in enumerate(lines):
            if re_title.match(line):
                lines[i] = line.lstrip()
        self.body = '\n'.join(lines)
        super().save(*args, **kwargs)

    # def body_to_html(self):
    #     return markdown.markdown(self.body,
    #                              extensions=[
    #                                  'extra',  # 基本扩展
    #                                  'codehilite',  # 代码高亮扩展
    #                                  'toc',  # 自动生成目录
    #                              ],
    #                              extension_configs={
    #                                  # 显示行号
    #                                  'codehilite': {'linenums': True, }
    #                              }
    #                              )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_at']
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Comment(m.Model):
    body = m.TextField()
    create_at = m.DateTimeField(auto_now_add=True)
    article = m.ForeignKey(Article, on_delete=m.CASCADE)
    parent = m.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=m.CASCADE)

    def __str__(self):
        return self.body[:20]

    class Meta:
        ordering = ['-create_at']
        verbose_name = '评论'
        verbose_name_plural = verbose_name
