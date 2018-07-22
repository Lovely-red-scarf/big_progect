# from django import template
#
# register = template.Library()
#
#
# from once.models import Category,Tag,Article,UserInfo
#
# from django.db.models import Count,Avg,Max
#
#
# @register.inclusion_tag('left_region.html')  #这个是先调用这个括号内的内容然后进行 加载完知乎再取下面的函数内找所需要的条件
#
# def get_query_data(username):
#
#     user = UserInfo.objects.filter(username = username).first()  #获取你当前登陆这个对象
#
#
#     blog = user.blog  #获取当前的博客
#
#     # 查询当前站点每一个分类的名称以及对应的文章数
#
#     cate_list = Category.objects.filter(blog = blog).annotate(c =Count('article__title')).value('title','c')
#
#     tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article__title")).values_list("title", "c")
#
#     # 日期归档
#
#     date_list = Article.objects.filter(user=user).extra(select={"y_m_date": "strftime('%%Y/%%m',create_time)"}).values(
#         "y_m_date").annotate(c=Count("title")).values_list("y_m_date", "c")
#     print(date_list)
#
#     return {"blog": blog, "username": username, "cate_list": cate_list, "tag_list": tag_list, "date_list": date_list}





from django import template

register=template.Library()

@register.simple_tag
def mul_tag(x,y):

    return x*y

from once.models import Category,Tag,Article,UserInfo
from django.db.models import Count,Avg,Max


@register.inclusion_tag("left_region.html")
def get_query_data(username):
    user = UserInfo.objects.filter(username=username).first()
    # 查询当前站点对象
    blog = user.blog

    # 查询当前站点每一个分类的名称以及对应的文章数

    cate_list = Category.objects.filter(blog=blog).annotate(c=Count("article__title")).values_list("title", "c")
    print(cate_list)

    # 查询当前站点每一个标签的名称以及对应的文章数

    tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article__title")).values_list("title", "c")

    # 日期归档

    date_list = Article.objects.filter(user=user).extra(select={"y_m_date": "strftime('%%Y/%%m',create_time)"}).values(
        "y_m_date").annotate(c=Count("title")).values_list("y_m_date", "c")
    print(date_list)

    return {"blog":blog,"username":username,"cate_list":cate_list,"tag_list":tag_list,"date_list":date_list}
