from django.shortcuts import render
from django.http import HttpResponse
from . import models


def article_list(request):
    articles = models.ArticlePost.objects.all()
    context = {'articles':articles}
    return render(request,'article/list.html',context)


def article_detail(request,id):
    article = models.ArticlePost.objects.get(id=id)
    context = {'article':article}
    return render(request,'article/detail.html',context)