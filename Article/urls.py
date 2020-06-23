from django.urls import path
from . import views

app_name = 'Article'

urlpatterns = [
    path('article-list/',views.article_list,name='article_list'),

]