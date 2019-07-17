from django.shortcuts import render, redirect
from .models import Article


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
    )
    print(articles)
    return render(request, 'index.html', {
        'articles': articles
    })


def about(request):
    return render(request, 'about.html')


def blog_list(request):
    return render(request, 'blog-list.html')


def detail(request):
    return render(request, 'detail.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return redirect('/index/')
