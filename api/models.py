from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

"""
博客功能分析:
    1.点赞功能  -->> 点赞表
    2.查询功能  -->> 文章表
    3.阅读功能  -->> 文章详情表
    4.评论功能  -->> 评论表
    5.分类功能  -->> 分类表
    6.注册登录功能    用户表
博客依赖表分析:
1.文章表
    文章标题
    发布时间
    阅读人数
    阅读数量
    点赞数量
    点踩数量
    评论数量
    文章内容
2.评论表
    评论时间
    评论人
    评论内容
    评论文章
3.点赞表
    点赞文章
    点赞用户
    点赞数量
    点踩数量
4.分类
    分类名称
"""

"""
1.文章表
    文章标题
    发布时间
    阅读人数
    阅读数量
    点赞数量
    点踩数量
    评论数量
    文章内容
"""


class User(models.Model):
    name = models.CharField(max_length=24, verbose_name="用户名")
    password = models.CharField(max_length=124, verbose_name="密码")
    avatar = models.ImageField(upload_to='avatar', verbose_name="头像")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '用户表'


class Article(models.Model):
    author = models.ForeignKey(verbose_name="作者", to="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=24, verbose_name="标题",unique=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    views = models.IntegerField(verbose_name="浏览量")
    good_num = models.IntegerField(verbose_name="点赞数量")
    bad_num = models.IntegerField(verbose_name="点踩数量")
    comment_num = models.IntegerField(verbose_name="评论数量")
    content = RichTextUploadingField(verbose_name="内容", config_name='ck')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name="文章分类")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '文章表'


"""
2.评论表
    评论时间
    评论人
    评论内容
    评论文章
"""


class Comment(models.Model):
    name = models.CharField(max_length=24, verbose_name="评论标题")
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, verbose_name='评论文章')
    user = models.ForeignKey(to='User', verbose_name="评论用户", on_delete=models.CASCADE)
    pu_date = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    content = RichTextUploadingField(verbose_name="评论内容", config_name='ck')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '评论表'


"""
3.点赞表
    点赞文章
    点赞用户
    点赞数量
    点踩数量
"""


class Good(models.Model):
    article = models.ForeignKey(to='Article', verbose_name="点赞文章", on_delete=models.CASCADE)
    user = models.ForeignKey(to="User", verbose_name="点赞用户", on_delete=models.CASCADE)
    good_num = models.IntegerField(verbose_name="点赞数量", default=0)
    bad_num = models.IntegerField(verbose_name="点踩数量", default=0)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = verbose_name_plural = '点赞表'


"""
4.分类
    分类名称
"""


class Category(models.Model):
    name = models.CharField(max_length=24, verbose_name="分类名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类表'
