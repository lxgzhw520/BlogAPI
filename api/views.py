from django.shortcuts import render, redirect
from .models import Article, Category, User, Good
# 导入分页函数
from libs.page import get_pagination_list
# 引入加密功能
from libs.lock import get_sha256


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
    # 刷新错误提示,防止重复出现的bug
    request.session['error'] = ''
    id = request.GET.get('id', 1)
    article = Article.objects.filter(id=id).first()
    # 浏览量增加的实现
    article.views += 1
    article.save()
    # 点赞和点踩的实现
    is_type = request.GET.get('type')
    if is_type:
        # 如果当前用户登录
        user = User.objects.filter(name=request.COOKIES.get('username')).first()
        if user:
            # 判断是否点赞过
            ret = Good.objects.filter(article=article, user=user)
            if not ret:
                # 根据点赞和踩进行增加
                if is_type == "good":
                    article.good_num += 1
                    article.save()
                    Good.objects.create(article=article,
                                        user=user,
                                        good_num=1,
                                        bad_num=0
                                        )
                if is_type == 'bad':
                    article.bad_num += 1
                    article.save()
                    Good.objects.create(article=article,
                                        user=user,
                                        good_num=0,
                                        bad_num=1
                                        )
            else:
                request.session['error'] = '您已经对这篇文字点赞或点踩过,不可重复提交哦~'
    return render(request, 'detail.html', {
        'article': article
    })


def register(request):
    # 注册功能的实现
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        avatar = request.FILES.get('avatar')
        # print(username, password, avatar)
        # 1.密码必须一致,长度大于6位
        # 2.密码加密
        # 3.确认数据库不存在该用户
        # 4.保存进数据库
        if password == password1 and len(password) > 5:
            password = get_sha256(password)
            if not User.objects.filter(name=username):
                # pass
                if User.objects.create(name=username, password=password, avatar=avatar):
                    return redirect('/login/')

    return render(request, 'register.html')


def login(request):
    # 登录功能的实现
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        agree = request.POST.get('agree')
        print(username, password, agree)
        # 1.密码加密
        # 2.去数据库查询比对
        # 3.判断是否需要七天免登陆
        password = get_sha256(password)
        user = User.objects.filter(name=username, password=password).first()
        if user:
            if agree:
                response = redirect('/index/')
                # 七天免登陆
                response.set_cookie("username", username, 3600 * 24 * 7)
                response.set_cookie("avatar", user.avatar, 3600 * 24 * 7)
                return response
            return redirect('/index/')
    return render(request, 'login.html')


def logout(request):
    response = redirect('/index/')
    # 删除cookie
    response.set_cookie('username', '', -1)
    response.set_cookie('avatar', '', -1)
    return response
