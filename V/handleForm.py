#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from M.models import UserMain
import time,hashlib

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=50)
    password = forms.CharField(label='password',widget=forms.PasswordInput())

def regist(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            check = UserMain.objects.filter(username__exact=username)
            if check:
                return HttpResponse('该用户名已存在,请更换用户名重试！')

            hash_obj = hashlib.md5()
            hash_obj.update(password.encode('utf-8'))
            md5_pwd = hash_obj.hexdigest()
            dateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            UserMain.objects.create(username=username,password=md5_pwd,date = dateTime)
            return HttpResponseRedirect('/login/')
    else:
        userform = UserForm()
    return render(request,'regist.html',{'userform':userform})

def login(request):
    if checkLoginStatus(request):
        response = HttpResponseRedirect('/')
        return response
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            hash_obj = hashlib.md5()
            hash_obj.update(password.encode('utf-8'))
            md5_pwd = hash_obj.hexdigest()

            user = UserMain.objects.filter(username__exact=username,password__exact=md5_pwd)

            if user:
                response = HttpResponseRedirect('/')
                response.set_cookie('username',username,3600)
                response.set_cookie('pwd',md5_pwd,3600)
                return response
            else:
                return HttpResponse('username/password error! please retry!')
    else:
        userform = UserForm()
    return render(request, 'login.html',{'userform':userform})

def logout(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('pwd')
    return response

# def index(request):
# 	username = request.COOKIES.get('username','')
# 	response = HttpResponseRedirect('/home/')
# 	return response

def checkLoginStatus(request):
	if (not 'username' in request.COOKIES) or (not 'pwd' in request.COOKIES):
		return False
	username = request.COOKIES['username']
	md5_pwd = request.COOKIES['pwd']
	user = UserMain.objects.filter(username__exact=username,password__exact=md5_pwd)
	if user:
		return True 
	else:
		return False
