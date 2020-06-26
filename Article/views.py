from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User
from . import forms


def article_list(request):
    articles = models.ArticlePost.objects.all()
    context = {'articles':articles}
    return render(request,'article/list.html',context)


def article_detail(request,id):
    article = models.ArticlePost.objects.get(id=id)
    context = {'article':article}
    return render(request,'article/detail.html',context)


def article_create(request):
    if request.method == 'POST':
        article_post_form = forms.article_post_form(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect('Article:article_list')
        else:
            return HttpResponse('the content of form is not valid. Please enter again')
    else:
        article_post_form = forms.article_post_form()
        context = {'article_post_form':article_post_form}
        return render(request,'article/create.html',context)


def article_delete(request,id):
    article = models.ArticlePost.objects.get(id=id)
    article.delete()
    return redirect('Article:article_list')
