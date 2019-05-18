#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from M.models import Bugs,UserMain,WordsMatch
from django import forms
import time

# Create your views here.
class UserForm(forms.Form):
    bugs = forms.CharField(widget=forms.Textarea) 

def bugs(request):
	if not checkLoginStatus(request):
		return HttpResponseRedirect('/login/')
	if request.method == 'POST':
		feedback = request.POST['feedback']
		dateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		username = request.COOKIES['username']
		Bitem = Bugs.objects.create(username=username,bugs=feedback,date=dateTime)
		return render(request,'bugs.html',{'result':'submitted!'})
	else:
		return render(request,'bugs.html')


def about(request):
	return render(request,'about.html')

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

def printout(request):
	if not checkLoginStatus(request):
		return HttpResponseRedirect('/login/')
	username = request.COOKIES['username']
	userAll = WordsMatch.objects.get(username__exact=username)
	en_str = userAll.english
	ch_str = userAll.chinese
	en_list = en_str.split('/')
	ch_list = ch_str.split('/')
	responseTable = []
	totalnum = len(en_list)
	for i in range(totalnum):
		s = en_list[i]+'\t'+ch_list[i]
		responseTable.append(s)
	return render(request,'print.html',{'table':responseTable,'totalnum':totalnum})

def printer(request):
	if not checkLoginStatus(request):
		return HttpResponseRedirect('/login/')
	username = request.COOKIES['username']
	userAll = WordsMatch.objects.get(username__exact=username)
	en_str = userAll.english
	er_str = userAll.errorrate
	tt_str = userAll.total
	en_list = en_str.split('/')
	er_list = er_str.split('/')
	tt_list = tt_str.split('/')
	responseTable = []
	totalnum = len(en_list)
	for i in range(totalnum):
		s = en_list[i]+'\t'+er_list[i]+'|'+tt_list[i]
		responseTable.append(s)
	return render(request,'printer.html',{'table':responseTable,'totalnum':totalnum})

def trans(request):
	import urllib.request
	from urllib.parse import quote
	import re
	import string
	target = request.GET.get('target')
	url = 'http://fy.webxml.com.cn/webservices/EnglishChinese.asmx/Translator?wordKey='+target
	q_url = quote(url,safe=string.printable)
	data=urllib.request.urlopen(q_url).read()
	record=data.decode('UTF-8')
	pattern = re.compile('<Translation>(.*)</Translation>')
	result = pattern.findall(record)  
	return render(request, 'trans.html',{'targetword':target,'translation':result[0]})
