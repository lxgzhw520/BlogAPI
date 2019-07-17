from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from BlogAPI import settings
from api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # 博客路由
    url(r'^index/$', views.index),
    url(r'^about/$', views.about),
    url(r'^blog/list/$', views.blog_list),
    url(r'^detail/$', views.detail),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
]
