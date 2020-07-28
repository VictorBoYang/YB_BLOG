from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User
from . import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from comment.models import Comment
from django.db.models import Q


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')

    if search:
        if order == 'total_views':
            article_list = models.ArticlePost.objects.filter(
                Q(title__icontains=search)|Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = models.ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = models.ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = models.ArticlePost.objects.all()
    # if request.GET.get('order') == 'total_views':
    #     article_list = models.ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     article_list = models.ArticlePost.objects.all()
    #     order = 'normal'

    # every page will show 3 articles
    paginator = Paginator(article_list, 3)

    page = request.GET.get('page')

    articles = paginator.get_page(page)

    context = {'articles': articles, 'order': order,'search': search}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = models.ArticlePost.objects.get(id=id)

    comments = Comment.objects.filter(article=id)

    # total_views auto increase
    article.total_views = article.total_views + 1
    article.save(update_fields=['total_views'])

    context = {'article': article, 'comments': comments}
    return render(request, 'article/detail.html', context)


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
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    article = models.ArticlePost.objects.get(id=id)
    # only the author of this article is allowed to delete this article
    if request.user != article.author:
        return HttpResponse('Sorry. You are not allowed to delete this article')
    article.delete()
    return redirect('Article:article_list')


def article_edit(request, id):
    article = models.ArticlePost.objects.get(id=id)

    # only the author of this article is allowed to edit this article
    if request.user != article.author:
        return HttpResponse('Sorry. You are not allowed to edit this article')

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
        context = {'article': article,
                   'article_post_form': article_post_form}
        return render(request, 'article/edit.html', context)
