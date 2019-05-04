from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.paginator import Paginator
from blog.models import Notice, Banner, User, Category, Tag, Article, Link
# Create your views here.


class IndexView(View):
    """首页"""
    def get(self, request):
        # 查出用户
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            pass
        # 查出所有分类
        categories = Category.objects.all()
        # 查出所有标签
        tags = Tag.objects.all()
        # 查出广告信息
        notices = Notice.objects.all()
        # 查出通知
        banners = Banner.objects.filter(is_delete=False)[:4]
        # 查出点击量前10的文章
        top_articles = Article.objects.get_top_articles()
        # 查出最新更新的10篇文章
        new_articles = Article.objects.get_new_articles()
        # 查出首页推荐的文章
        recommend_articles = Article.objects.get_recommend_articles(recommend=2)
        # 随机推荐文章
        interesting_articles = Article.objects.all().order_by('?')[:5]
        # 查出所有友情链接
        links = Link.objects.all()

        # 整理上下文
        context = {
            'user': user,
            'categories': categories,
            'tags': tags,
            'notices': notices,
            'banners': banners,
            'top_articles': top_articles,
            'new_articles': new_articles,
            'recommend_articles': recommend_articles,
            'interesting_articles': interesting_articles,
            'links': links,
            'page': 'index',
        }

        return render(request, 'index.html', context)


class DetailView(View):
    """文章详细内容"""
    def get(self, request, article_id):
        # 查出用户
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            pass

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return render(reverse('blog:index'))
        # 查出该文章的上一篇
        prev_article = Article.objects.filter(create_time__gt=article.create_time, category=article.category.id).first()
        # 查出该文章的下一篇
        next_article = Article.objects.filter(create_time__lt=article.create_time, category=article.category.id).last()
        # 查出所有分类
        categories = Category.objects.all()
        # 查出所有标签
        tags = Tag.objects.all()
        # 查出文章的分类
        category = article.category
        # 查出点击量前十的文章
        top_articles = Article.objects.get_top_articles()
        # 查出最新更新的5篇文章
        new_articles = Article.objects.get_new_articles()
        # 查出热门推荐的文章
        recommend_articles = Article.objects.filter(category=category,recommend=1)
        # 随机推荐文章
        interesting_articles = Article.objects.all().order_by('?')[:5]

        article.read += 1
        article.save()
        # 整理上下文
        context = {
            'user': user,
            'article': article,
            'prev_article': prev_article,
            'next_article': next_article,
            'categories': categories,
            'tags': tags,
            'page': category,
            'top_articles': top_articles,
            'new_articles': new_articles,
            'recommend_articles': recommend_articles,
            'interesting_articles': interesting_articles,
        }
        return render(request, 'detail.html', context)


class IntroductionView(View):
    """自我介绍"""
    def get(self, request):
        # 查出所有分类
        categories = Category.objects.all()
        user = User.objects.get(username='黄先森')
        context = {
            'user': user,
            'page': 'introduction',
            'categories': categories,
        }
        return render(request, 'introduction.html', context)


class CategoryListView(View):
    # 分类列表
    def get(self, request, category_id, page_id):
        # 查出用户
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            return redirect(reverse('blog:index'))
        # 查出所有分类
        categories = Category.objects.all()
        # 查出用户点击的分类
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return redirect(reverse('blog:index'))
        # 查出所有标签
        tags = Tag.objects.all()
        # 查出该分类下的所有文章
        articles = Article.objects.filter(category=category)
        # 查出点击量前10的文章
        top_articles = Article.objects.get_top_articles()
        # 查出最新更新的10篇文章
        new_articles = Article.objects.get_new_articles()
        # 查出热门推荐的文章
        recommend_articles = Article.objects.filter(category=category,recommend=1)
        # 随机推荐文章
        interesting_articles = Article.objects.all().order_by('?')[:5]

        paginator = Paginator(articles, 1)
        # 判断页码是否规范
        try:
            page = int(page_id)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1
        # 自定义分页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif page > num_pages - 2:
            pages = range(num_pages - 4, num_pages)
        else:
            pages = range(num_pages - 2, num_pages + 3)

        page_data = paginator.page(page)

        context = {
            'user': user,
            'categories': categories,
            'category': category,
            'tags': tags,
            'top_articles': top_articles,
            'new_articles': new_articles,
            'recommend_articles': recommend_articles,
            'interesting_articles': interesting_articles,
            'page': category,
            'pages': pages,
            'page_data': page_data,
        }
        return render(request, 'category_list.html', context)


class TagListView(View):
    # 分类列表
    def get(self, request, tag_id, page_id):
        # 查出用户
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            return redirect(reverse('blog:index'))
        # 查出所有分类
        categories = Category.objects.all()
        # 查出用户点击的tag
        tag = Tag.objects.get(id=tag_id)
        # 查出所有标签
        tags = Tag.objects.all()
        # 查出该标签下的所有文章
        articles = Article.objects.filter(tags=tag)
        # 查出点击量前10的文章
        top_articles = Article.objects.get_top_articles()
        # 查出最新更新的10篇文章
        new_articles = Article.objects.get_new_articles()
        # 查出热门推荐的文章
        recommend_articles = Article.objects.filter(tags=tag,recommend=1)
        # 随机推荐文章
        interesting_articles = Article.objects.all().order_by('?')[:5]

        paginator = Paginator(articles, 1)
        # 判断页码是否规范
        try:
            page = int(page_id)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1
        # 自定义分页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages+1)
        elif page <=3:
            pages = range(1, 6)
        elif page > num_pages-2:
            pages = range(num_pages-4, num_pages)
        else:
            pages = range(num_pages-2, num_pages+3)

        page_data = paginator.page(page)

        context = {
            'user': user,
            'categories': categories,
            'tag': tag,
            'tags': tags,
            'articles': articles,
            'top_articles': top_articles,
            'new_articles': new_articles,
            'recommend_articles': recommend_articles,
            'interesting_articles': interesting_articles,
            'page': tag,
            'pages': pages,
            'page_data': page_data
        }
        return render(request, 'tag_list.html', context)


class SearchView(View):
    """搜索视图"""
    def get(self, request):
        keyword = request.GET.get('q')
        articles = Article.objects.filter(title__icontains=keyword)
        print('*'*10, articles)
        # 查出用户
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            return redirect(reverse('blog:index'))
        # 查出所有分类
        categories = Category.objects.all()
        # 查出所有标签
        tags = Tag.objects.all()
        # 查出点击量前10的文章
        top_articles = Article.objects.get_top_articles()
        # 查出最新更新的10篇文章
        new_articles = Article.objects.get_new_articles()
        # 查出热门推荐的文章
        recommend_articles = Article.objects.filter(recommend=1)
        # 随机推荐文章
        interesting_articles = Article.objects.all().order_by('?')[:5]

        context = {
            'user': user,
            'categories': categories,
            'tags': tags,
            'top_articles': top_articles,
            'new_articles': new_articles,
            'recommend_articles': recommend_articles,
            'interesting_articles': interesting_articles,
            'articles': articles,

        }

        return render(request, 'search.html', context)