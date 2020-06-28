from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from . import forms


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
