#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django import forms
from M.models import WordsMatch,UserMain
import time,json

# Create your views here.
class UserForm(forms.Form):
    enwords = forms.CharField(label='enwords',max_length=50)
    chwords = forms.CharField(label='chwords',max_length=50)

class ExamForm(forms.Form):
    enwords = forms.CharField(label='enwords',max_length=50)


def homepage(request):
	if not checkLoginStatus(request):
		return render(request, 'mainpage.html',{'needlogin':1})
	else:
		return render(request, 'mainpage.html',{'needlogin':0})

def record(request):
	if not checkLoginStatus(request):
		return HttpResponseRedirect('/login/')
	if request.method == 'POST':
		userform = UserForm(request.POST)
		if userform.is_valid():
			en = userform.cleaned_data['enwords']
			ch = userform.cleaned_data['chwords']
			dateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			username = request.COOKIES['username']
			if not WordsMatch.objects.filter(username=username):
				WordsMatch.objects.create(username=username,english=en,chinese=ch,date=dateTime,errorrate=0,process_tag=0,total=0,wordid=1)
			else:
				responseItem = WordsMatch.objects.get(username=username)
				en_str = responseItem.english
				ch_str = responseItem.chinese
				er_str = responseItem.errorrate
				tt_str = responseItem.total
				wi_str_toprocess = responseItem.wordid
				wi_templist = wi_str_toprocess.split('/')
				lastwi = int(wi_templist[-1])
				wi_str = str(lastwi+1)
				responseItem.english = en_str+'/'+en
				responseItem.chinese = ch_str+'/'+ch
				responseItem.errorrate = er_str+'/0'
				responseItem.total = tt_str+'/0'
				responseItem.wordid = wi_str_toprocess+'/'+wi_str
				responseItem.date = dateTime
				responseItem.save()
			return render(request,'mainpage.html',{'userform':userform,'recordResult':'添加成功!'})
		else:
			return HttpResponse("<p>记录异常!请与管理员联系！</p>")
	return render(request,'mainpage.html',{'userform':userform})

def exam(request):
	if not checkLoginStatus(request):
		return HttpResponseRedirect('/login/')
	return render(request,'exam.html')

def getword(request):
	responseData = {}
	username = request.COOKIES['username']
	cnt = int(request.GET.get('cnt'))
	cnt *=20
	responseItem = WordsMatch.objects.get(username=username)
	en = responseItem.english
	ch = responseItem.chinese
	er = responseItem.errorrate
	wi = responseItem.wordid
	responseItem.process_tag = cnt
	responseItem.save()
	enList = en.split('/')
	chList = ch.split('/')
	erList = er.split('/')
	wiList = wi.split('/')
	responseData['en'],responseData['ch'],responseData['wi'] = shuffle(enList[cnt:(cnt+20)], chList[cnt:(cnt+20)], erList[cnt:(cnt+20)], wiList[cnt:(cnt+20)])
	return JsonResponse(responseData) 

def shuffle(a, b, c, d):
	import random
	examCnt = []	#存放呈现次数
	o_a = []
	o_b = []
	o_d = []
	show_a = []
	show_b = []
	show_d = []

	for i in range(len(c)):
		showCnt = errorRateMap(float(c[i]))
		examCnt.append(showCnt)
		for j in range(showCnt):
			o_a.append(a[i])
			o_b.append(b[i])
			o_d.append(d[i])

	idList = [k for k in range(len(o_a))]
	random.shuffle(idList)
	for s in idList:
		show_a.append(o_a[int(s)])
		show_b.append(o_b[int(s)])
		show_d.append(o_d[int(s)])
	return show_a,show_b,show_d

def errorRateMap(x):
	return int(5*(x**2)+1)

def calculate(request):
	cons_json = request.GET.get('consequence')
	json_dic = json.loads(cons_json)
	username = request.COOKIES['username']
	responseItem = WordsMatch.objects.get(username=username)
	rr = responseItem.errorrate
	tt = responseItem.total
	rrList = rr.split('/')
	ttList = tt.split('/')
	for d in json_dic:
		id_key = int(d)
		rr_toadd = float(json_dic[d].split('/')[0])	#error rate
		tt_toadd = int(json_dic[d].split('/')[1])	#total
		new_rr_ori = (float(rrList[id_key-1])*float(ttList[id_key-1])+rr_toadd)/(tt_toadd+int(ttList[id_key-1]))
		new_rr = round(new_rr_ori,3)
		rrList[id_key-1] = new_rr
		ttList[id_key-1] = int(ttList[id_key-1])+tt_toadd
	r_temp = [i for i in map(str,rrList)]
	t_temp = [j for j in map(str,ttList)]
	responseItem.errorrate = '/'.join(r_temp)
	responseItem.total = '/'.join(t_temp)
	responseItem.save()
	return HttpResponse('success');

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