from django.shortcuts import render,redirect,HttpResponse,reverse

# Create your views here.



from once.models import UserInfo,Article,Comment,Blog,Article2Tag,ArticleUpDown,Category,Tag


from django.contrib import auth  #导入auth模块
def login(request):
    '''
    登陆
    :param request:
    :return:
    '''
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = auth.authenticate(username =user,password=pwd)  #自动给你的user表自动校验
        if user: #登陆成功
            auth.login(request,user)  #相当于设置session
            return redirect('/index/')
        print(333333333333)
    return render(request,'login.html')



def index(request):
    '''
    主界面
    :param request:
    :return:
    '''
    article_list = Article.objects.all()

    return render(request,'index.html',locals())





def logout(request):
    '''
    注销
    :param request:
    :return:
    '''

    auth.logout(request)
    return redirect('/login/')




def homesite(request,username,**kwargs):

    user = UserInfo.objects.filter(username = username ).first()  #求出登陆的对象
    blog = user.blog   #登陆人的博客


    # if not kwargs:  #如果没有这个kwargs  也就是值输入了用户名 只查看 这个人的文章
    #     article_list = Article.objects.filter(user__username = username)   #求没有后面的选项的文章
    # else:
    #     #如果有后面的最后选项
    #     condition = kwargs.get('condition')
    #     params = kwargs.get('parmas')
        # if condition == 'category':  #如果输入的是正确
        #     Article_list = Article.objects.filter(user__username = username).filter(category__title = params )
        #
        #
        # elif condition == 'tag':
        #     Article_list = Article.objects.filter(user__username =username).filter(tag__title = params)

    if not kwargs:
        article_list = Article.objects.filter(user__username=username)

    else:
        condition = kwargs.get("condition")
        params = kwargs.get("params")

        if condition == "category":
            article_list = Article.objects.filter(user__username=username).filter(category__title=params)
        elif condition == "tag":
            article_list = Article.objects.filter(user__username=username).filter(tags__title=params)
        else:
            year, month = params.split("/")
            article_list = Article.objects.filter(user__username=username).filter(create_time__year=year,
                                                                                  create_time__month=month)

    if not article_list:
        return render(request,'not_font.html')

    return render(request, 'homesite.html', locals())





def article_detail(request,username,article_id):
    '''
    文章详情页面
    :param request:
    :return:
    '''
    user = UserInfo.objects.filter(username = username).first()

    blog = user.blog
    article_obj = Article.objects.filter(pk = article_id).first()


    comment_list = Comment.objects.filter(article_id=article_id)
    # comment_list= Comment.objects.filter(article_id = article_id)

    return render(request,'article_detail.html',locals())

from django.http import JsonResponse  #这是一个可以直接吧你的字典以序列化形式发送过去 内部序列化 然后  对方接收无序反序列化

from django.db.models import F   #可以直接把你的orm中字段作为变量处理
from django.db import transaction  #可以设置事务
import json

def praise(request):

    is_up = json.loads(request.POST.get('is_up'))
    article_id = request.POST.get('article_id')
    user_id = request.user.pk
    response = {'state': True, 'msg': None}

    obj = ArticleUpDown.objects.filter(user_id = user_id,pk=article_id).first()  #判断这个人是否对这个文章进行过操作

    if obj:  #操作过
        response['handled'] = obj.is_up
        response['state'] = False

    else:  #没有操作过
        with transaction.atomic():  #设置事务

            new_obj = ArticleUpDown.objects.create(user_id = user_id,pk=article_id,is_up=is_up)
            # if is_up:  #点赞
            #     Article.objects.filter(pk =article_id).update(up_count = F('up_count')+1)
            # else:
            #     Article.objects.filter(pk = article_id).update(down_count = F('down_count')+1)

            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    return JsonResponse(response)


def comment(request):

    # 获取数据
    user_id=request.user.pk
    article_id=request.POST.get("article_id")
    content=request.POST.get("content")
    pid=request.POST.get("pid")
    # 生成评论对象
    with transaction.atomic():
        comment=Comment.objects.create(user_id=user_id,article_id=article_id,content=content,parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)

    response={"state":True}
    response["timer"]=comment.create_time.strftime("%Y-%m-%d %X")
    response["content"]=comment.content
    response["user"]=request.user.username #全局取登陆人的名字

    return JsonResponse(response)




# def backend(request):
#     print('kkkkkkkkkkkkkkkkkkkkkk')
#
#
#     user = request.user
#
#
#     article_list = Article.objects.filter(user = user)
#
#
#     return render(request,'backend/backend.html',locals())





def backend(request):
    user=request.user
    article_list=Article.objects.filter(user=user)
    return render(request,"backend/backend.html",locals())




#
# def add_article(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         user = request.user
#         cate_pk = request.POST.get('cate_pk')
#         tags_pk_list = request.POST.getlist("tags")   # 标签有多个
#
#         # desc = content[0:150]  #摘要 我们设置取文章的前150个字符
#
#         from bs4 import BeautifulSoup  #这是一个防止xss攻击 还可以向像正则一样匹配我们所需要的字符或者标签
#         soup = BeautifulSoup(content,'html.parser')   #  去除你content中 就是你全文中的html标签
#
#         for tag in soup.find_all():
#             if tag.name in ['script']:
#                 tag.decompse()
#
#         # 切片文章文本
#         desc = soup.text[0:150]
#
#
#     else:
#         user = request.user
#         blog =user.blog
#         cate_list = Category.objects.filter(blog=blog)
#         tags = Tag.objects.filter(blog=blog)
#
#     return render(request,'backend/add_article.html',locals())



from  two import settings
import os
def upload(request):
    obj = request.FILES.get('upload_img')   #这个是从fiels内取这个文件

    name = obj.name


    path = os.path.join (settings.BASE_DIR,'static','upload',name)

    with open(path,'wb') as f:
        for line in obj:
            f.write(line)


        res = {
            'error':0,
            'url':'/static/upload/upload'+name
        }


    return JsonResponse(res)   #用JsonResponse 这个模块来进行模块的设置


def backend(request):
    user = request.user
    article_list = Article.objects.filter(user=user)
    return render(request, "backend/backend.html", locals())


def add_article(request):
    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.user
        cate_pk = request.POST.get("cate")
        tags_pk_list = request.POST.getlist("tags")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")  # 去除你content中 就是你全文中的html标签
        # 文章过滤：
        for tag in soup.find_all():  # 查找全文的所有的标签
            # print(tag.name)
            if tag.name in ["script", ]:  # 如果你的 全局标签内 有script标签 防止别人控制你的浏览器就删除script标签
                tag.decompose()

        # 切片文章文本
        desc = soup.text[0:150]

        article_obj = Article.objects.create(title=title, content=str(soup), user=user, category_id=cate_pk, desc=desc)

        for tag_pk in tags_pk_list:
            Article2Tag.objects.create(article_id=article_obj.pk, tag_id=tag_pk)

        return redirect("/backend/")

    else:
        blog = request.user.blog
        cate_list = Category.objects.filter(blog=blog)
        tags = Tag.objects.filter(blog=blog)
        return render(request, "backend/add_article.html", locals())


from two import settings
import os


# def upload(request):
#     print(request.FILES)
#     obj = request.FILES.get("upload_img")
#     name = obj.name
#
#     path = os.path.join(settings.BASE_DIR, "static", "upload", name)
#     with open(path, "wb") as f:
#         for line in obj:
#             f.write(line)
#
#     import json
#
#     res = {
#         "error": 0,
#         "url": "/static/upload/" + name
#     }
#
#     return HttpResponse(json.dumps(res))
