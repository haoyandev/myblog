from django.contrib import admin
from blog.models import Notice, Banner, Recommend, Category, Tag, Article, User, Link
# Register your models here.

admin.site.register(Banner)
admin.site.register(Notice)
admin.site.register(Recommend)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(User)
admin.site.register(Link)
