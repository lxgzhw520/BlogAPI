# _*_ coding:UTF-8 _*_
# 开发人员: 理想国真恵玩-张大鹏
# 开发团队: 理想国真恵玩
# 开发时间: 2019-07-17 13:32
# 文件名称: libs.py
# 开发工具: PyCharm

# 封装分页函数
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_pagination_list(articles, p):
    # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    paginator = Paginator(articles, 5)
    try:
        # 获取当前页码的记录
        articles = paginator.page(p)
    except PageNotAnInteger:
        # 如果用户输入的页码不是整数时,显示第1页的内容
        articles = paginator.page(1)
    except EmptyPage:
        # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        articles = paginator.page(paginator.num_pages)
    return articles
