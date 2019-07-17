from django.contrib import admin
from .models import User, Article, Category, Comment, Good

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Good)
