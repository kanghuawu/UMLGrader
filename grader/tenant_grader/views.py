
from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import TenantData, TenantFields, TenantTable
from .form import GradeForm, ClassSeqDiagram
import subprocess as sp
import json
import os
import os.path as osp
import zipfile
from django.contrib.auth.decorators import login_required
import time

tenant_id='khwu'
newfilelocation = ''
@login_required
def loginredirect(request):
	# print user.username
	url = '/grader/%s/' % request.user.username
	return HttpResponseRedirect(url)


@login_required
def grader(request, username='khwu'):
	print username
	grade_title, grade_result = getGradesFromDB()
	radio = ClassSeqDiagram()
	file = uploadFile(request)
	# form = updateForm(request)
	# if request.POST:
	# 	return HttpResponseRedirect(reverse("grader"))
	# print request.POST['choice_field'] == '1'
	if request.method == 'POST' and 'form_sub' in request.POST:
		form = GradeForm(request.POST)
		new_grade = form.save(commit=False)
		new_grade.record_id = TenantData.objects.filter(tenant_id=tenant_id).count() + 1	
		new_grade.tenant_id = tenant_id
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("grader"))
	else:
		form = GradeForm()

	context = {
		'radio': radio,
		'uploaded_file_url': file,
		'title': grade_title,
		'result': grade_result,
		'form' : form
	}
	return render(request, 'tenant_grader/graderpage.html', context)

def getGradesFromDB(tenant_id='khwu'):
	TF = TenantFields.objects.filter(tenant_id=tenant_id).order_by('field_column')
	TF_name = list(TF.values_list('field_name', flat=True))
	grade_title = ['Record Number']
	grade_title.extend(list(TF_name))
	grade_result = []
	for TD in TenantData.objects.filter(tenant_id=tenant_id).order_by('record_id'):
		grade_result.append(TD.getFields(TF.count() + 1))
	return grade_title, grade_result

# reference: https://github.com/sibtc/simple-file-upload.git
def uploadFile(request):
    if request.method == 'POST' and request.FILES and request.FILES['myfile']:
    	cleanFile()
    	diagram_type = request.POST['choice_field']
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        newfilelocation = parseJavaFile(diagram_type, filename)
        uploaded_file_url = fs.url(filename)
        # print filename
        # print uploaded_file_url
    	return newfilelocation
    elif request.method == 'POST' and not request.FILES:
    	return "Please select a file"

def updateForm(request, tenant_id='khwu'):
	if request.method == 'POST' and 'form_sub' in request.POST:
		form = GradeForm(request.POST)
		new_grade = form.save(commit=False)
		new_grade.record_id = TenantData.objects.filter(tenant_id=tenant_id).count() + 1	
		new_grade.tenant_id = tenant_id
		if form.is_valid():
			form.save()
	else:
		form = GradeForm()
	return form

USER = osp.join(osp.expanduser('~'), tenant_id)
MEDIA = osp.join(os.getcwd(), 'media')
STATIC = osp.join(os.getcwd(), 'static', 'tenant_grader')
JAR = osp.join(USER, 'class', 'umlparser.jar')
CLASS = osp.join(USER, 'class', 'class')
SEQ = osp.join(USER, 'seq', 'sequence')
SEQ_MAKE = osp.join(USER, 'seq')
OUTPUT = osp.join(USER, 'output')

def parseJavaFile(diagram_type, filename):
	if diagram_type == '1':
		unzipFile(osp.join(MEDIA, filename), CLASS)
		sp.call(["java", "-jar", JAR, CLASS, osp.join(OUTPUT, 'output.png')])
	else:
		print filename
		unzipFile(osp.join(MEDIA, filename), SEQ)
		sp.call(["make", "-C", SEQ_MAKE, 'demo'])
	timestr = time.strftime("%Y%m%d-%H%M%S")
	newfile = osp.join(MEDIA, timestr+'.png')
	sp.call(["cp", osp.join(OUTPUT, 'output.png'), newfile])
	return timestr+'.png'
		
		
def unzipFile(curdir, extractdir):
	sp.call(["unzip", "-j", curdir, '-d', extractdir])

	# zip_ref = zipfile.ZipFile(curdir, 'r')
	# zip_ref.extractall(extractdir)
	# zip_ref.close()

def cleanFile():
	sp.call(["make", "-C", SEQ_MAKE, 'clean'])
	sp.call(["rm", "-rf", MEDIA])
	sp.call(["mkdir", MEDIA])
	sp.call(["rm", "-rf", CLASS])
	sp.call(["mkdir", CLASS])
	sp.call(["rm", "-rf", SEQ])
	sp.call(["mkdir", SEQ])
	sp.call(["rm", "-rf", OUTPUT])
	sp.call(["mkdir", OUTPUT])


