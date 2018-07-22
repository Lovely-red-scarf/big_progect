"""two URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from once import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),  #登陆
    path('index/',views.index, name='index'),  #主界面
    path('logout/',views.logout, name='logout'),  #注销


    # re_path('(?P<username>\w+)/article/(?P<article_id>\d+)/',views.article_detail),
    # re_path('(?P<usernmae>w+)/(?P<condition>category|tag|achrive)/(?P<params>.*)',views.homesite),  #输入用户的选择查看的内容
    #
    # re_path('(?P<username>\w+)/', views.homesite),
    # # re_path('(?P<username>\w+)/$', views.homesite),

    path('praise/',views.praise),  #这是点赞的url

    path('comment/',views.comment),  #这是评论url

    path('backend/',views.backend),  #这个是后台管理的显示界面

    path('add_article/',views.add_article, name='add_article') , #添加文章

    path('upload/',views.upload),  # 这个是上传文件的时候弄的

    re_path('(?P<username>\w+)/article/(?P<article_id>\d+)$', views.article_detail),
    # 跳转
    re_path('(?P<username>\w+)/(?P<condition>category|tag|achrive)/(?P<params>.*)', views.homesite),
    # 个人站点
    re_path('(?P<username>\w+)/$', views.homesite),

]
