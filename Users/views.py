from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from . import forms
from .models import *
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        user_login_form = forms.user_login_form(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect('Article:article_list')
            else:
                return HttpResponse('Username or password is wrong,please enter again.')
        else:
            return HttpResponse('Username or password is not valid')
    elif request.method == 'GET':
        user_login_form = forms.user_login_form()
        context = {'form':user_login_form}
        return render(request,'user/login.html',context)
    else:
        return HttpResponse('Please use GET or POST to request data')


def user_logout(request):
    logout(request)
    return redirect('Article:article_list')


def user_register(request):
    if request.method == 'POST':
        user_register_form = forms.user_register_form(data = request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request,new_user)
            return redirect('Article:article_list')
        else:
            return HttpResponse('Register forms wrong. Please try again.')
    elif request.method == 'GET':
        user_register_form = forms.user_register_form()
        context = { 'form':user_register_form }
        return render(request,'user/register.html',context)
    else:
        return HttpResponse('Please use GET or POST to request data')


@login_required(login_url='/Users/login')
def profile_edit(request,id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse('You are not allowed to edit this user')
        profile_form = forms.profile_form(request.POST,request.FILES)
        if profile_form.is_valid():
            profile.phone = profile_form.cleaned_data['phone']
            profile.description = profile_form.cleaned_data['description']
            if 'photo' in request.FILES:
                profile.photo = profile_form.cleaned_data['photo']
            profile.save()
            return redirect('Users:edit',id=id)
        else:
            return  HttpResponse('Form is not vaild. Please enter again')
    elif request.method == 'GET':
        profile_form = forms.profile_form()
        context = {'profile_form':profile_form,'profile':profile,'user':user}
        return render(request,'user/edit.html',context)
    else:
        return HttpResponse('Please use POST or GET request')
