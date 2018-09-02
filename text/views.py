from django.shortcuts import render
from django.http import HttpResponse
import time
import subprocess
import os
# Create your views here.

def input(request):
	return render(request,'text/input.html')

def index(request):
	info=[]
	for k in request.POST.keys():
		if k!='csrfmiddlewaretoken':
			info.append(request.POST[k])
	curr_path = os.path.dirname(__file__)
	c_path = os.path.join(curr_path,'web_courses.py')
	args = ['python.exe', c_path]
	args.extend(info)
	subprocess.Popen(args)
	return HttpResponse("Your request is being processed. Kick back, relax, and we'll let you know when there's an opening.")
	