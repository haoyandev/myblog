from django.conf.urls import url
from apps.blog.views import IndexView, IntroductionView, CategoryListView, DetailView, TagListView, SearchView

urlpatterns = [

    url(r'^index$', IndexView.as_view(), name='index'),  # 首页
    url(r'^introduction$', IntroductionView.as_view(), name='introduction'),  # 关于我
    url(r'^list/category/(?P<category_id>\d+)/(?P<page_id>\d+)$', CategoryListView.as_view(), name='category_list'),  # 分类列表
    url(r'^list/tag/(?P<tag_id>\d+)/(?P<page_id>\d+)$', TagListView.as_view(), name='tag_list'),  # 标签列表
    url(r'^detail/(?P<article_id>\d+)$', DetailView.as_view(), name='detail'),  # 文章详细
    url(r'^search$', SearchView.as_view(), name='search'),  # 搜索
]
