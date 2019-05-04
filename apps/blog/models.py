from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from db.base_models import BaseModel
from tinymce.models import HTMLField
# Create your models here.


class User(AbstractUser, BaseModel):
    """用户模型"""
    introduction = HTMLField(max_length=200, default='', verbose_name='自我介绍')
    introduction_detail = HTMLField(max_length=500, default='', verbose_name='自我介绍详情')
    head_img = models.ImageField(upload_to='blog', verbose_name='头像', default='')
    code = models.ImageField(upload_to='blog', verbose_name='二维码', default='')
    job = models.CharField(max_length=100, verbose_name='职业', default='')
    address = models.CharField(max_length=200, default='', verbose_name='住址')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Category(BaseModel):
    # 博客分类模型
    name = models.CharField(max_length=20, verbose_name='种类名称')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


class Tag(BaseModel):
    # 文章标题模型
    name = models.CharField(max_length=20, verbose_name='文章标题')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name


class Recommend(BaseModel):
    # 推荐位模型
    name = models.CharField(max_length=20, verbose_name='推荐位')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'recommend'
        verbose_name = '推荐位'
        verbose_name_plural = verbose_name


class ArticleManager(models.Manager):
    # 文章管理类
    def get_top_articles(self):
        # 查出前10的篇文章
        top_articles = self.all().order_by('-read')[:10]
        return top_articles

    def get_new_articles(self):
        # 查出最新更新的10篇文章
        new_articles = self.all().order_by('-create_time')[:10]
        return new_articles

    def get_recommend_articles(self, recommend):
        # 查出对应推荐位的文章
        recommend_articles = self.filter(recommend=recommend)
        return recommend_articles


class Article(BaseModel):
    # 文章模型
    title = models.CharField(max_length=100, verbose_name='标题')
    digest = models.TextField(verbose_name='摘要', blank=True)
    content = HTMLField(verbose_name='内容', blank=True)
    img = models.ImageField(upload_to='blog', default='', blank=True)
    read = models.IntegerField(default=0, verbose_name='阅读量')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    category = models.ForeignKey(Category, verbose_name='文章分类')
    recommend = models.ForeignKey(Recommend, default='', verbose_name='推荐位', blank=True)
    author = models.ForeignKey(User, verbose_name='作者')
    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    # 广告横幅模型
    url = models.CharField(max_length=255, verbose_name='链接')
    alt = models.CharField(max_length=40, verbose_name='链接说明', blank=True)
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    img = models.ImageField(upload_to='banner', verbose_name='广告图片')

    def __str__(self):
        return self.alt

    class Meta:
        db_table = 'banner'
        verbose_name = '广告'
        verbose_name_plural = '广告'


class Notice(BaseModel):
    # 通知模型
    url = models.CharField(max_length=255, verbose_name='链接')
    title = models.CharField(max_length=40, verbose_name='链接说明')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    img = models.ImageField(upload_to='banner', verbose_name='通知图片')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notice'
        verbose_name = '通知'
        verbose_name_plural = verbose_name


class Link(BaseModel):
    # 友情链接
    url = models.CharField(max_length=255, verbose_name='链接')
    title = models.CharField(max_length=20, verbose_name='链接说明')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'link'
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
