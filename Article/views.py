from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User
from . import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def article_list(request):
    article_list = models.ArticlePost.objects.all()

    # every page will show 6 articles
    paginator = Paginator(article_list,2)

    page = request.GET.get('page')

    articles = paginator.get_page(page)

    context = {'articles':articles}
    return render(request,'article/list.html',context)


def article_detail(request,id):
    article = models.ArticlePost.objects.get(id=id)
    context = {'article':article}
    return render(request,'article/detail.html',context)


@login_required(login_url='Users/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = forms.article_post_form(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
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


def article_edit(request,id):
    article = models.ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = forms.article_post_form(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('Article:article_detail', id=id)
        else:
            return HttpResponse('the content of form is not valid. Please enter again')
    else:
        article_post_form = forms.article_post_form()
        context = {'article':article,
                   'article_post_form':article_post_form}
        return render(request,'article/edit.html',context)
