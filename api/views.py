from django.shortcuts import render, redirect
from .models import Article, Category
# 导入分页函数
from .libs import get_pagination_list


# Create your views here.
def index(request):
    articles = Article.objects.values(
        'id',
        'img',
        'name',
        'desc',
        'pub_date',
        'views',
        'comment_num',
        'category'
    ).order_by('-pub_date')[0:20]
    return render(request, 'index.html', {
        'articles': articles
    })


def about(request):
    return render(request, 'about.html')


def blog_list(request):
    # 所有分类
    categorys = Category.objects.all()
    # 分类id
    id = request.GET.get('id', 1)
    # 文章 分页前必须对文章进行排序
    articles = Article.objects.filter(category__id=id).order_by('-pub_date')

    # 搜索功能的实现
    if request.method == "POST":
        search = request.POST.get("search")
        # 根据浏览人数降序
        articles = Article.objects.filter(name__contains=search).order_by('-views')

    # 分页的实现
    p = request.GET.get('p')  # 在URL中获取当前页面数
    # 调用分页函数
    articles = get_pagination_list(articles, p)
    return render(request, 'blog-list.html', {
        'categorys': categorys,
        'articles': articles
    })


def detail(request):
    id = request.GET.get('id', 1)
    article = Article.objects.filter(id=id).first()
    return render(request, 'detail.html', {
        'article': article
    })


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return redirect('/index/')
