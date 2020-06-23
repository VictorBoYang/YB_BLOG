from django.shortcuts import render
from django.http import HttpResponse
from . import models


def article_list(request):
    articles = models.ArticlePost.objects.all()
    context = {'articles':articles}
    return render(request,'article/list.html',context)