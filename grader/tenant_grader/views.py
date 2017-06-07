
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
import boto3

@login_required
def loginredirect(request):
	# print user.username
	url = '/grader/%s/' % request.user.username
	return HttpResponseRedirect(url)


@login_required
def grader(request, username):
	global thisuser
	thisuser = username

	global USER, MEDIA, STATIC, JAR, CLASS, SEQ, SEQ_MAKE, OUTPUT
	USER = osp.join(osp.expanduser('~'), username)
	MEDIA = osp.join(os.getcwd(), 'media')
	STATIC = osp.join(os.getcwd(), 'static')
	JAR = osp.join(USER, 'class', 'umlparser.jar')
	CLASS = osp.join(USER, 'class', 'class')
	SEQ = osp.join(USER, 'seq', 'sequence')
	SEQ_MAKE = osp.join(USER, 'seq')
	OUTPUT = osp.join(USER, 'output')


	grade_title, grade_result = getGradesFromDB(tenant_id=username)
	diagram_type = ClassSeqDiagram()
	new_file = uploadFile(request)
	if request.method == 'POST' and 'form_sub' in request.POST:
		form = GradeForm(request.POST)
		new_grade = form.save(commit=False)
		new_grade.record_id = TenantData.objects.filter(tenant_id=username).count() + 1	
		new_grade.tenant_id = username
		if form.is_valid():
			form.save()
			url = '/grader/%s/' % request.user.username
			return HttpResponseRedirect(url)
	else:
		form = GradeForm()

	context = {
		'diagram_type': diagram_type,
		'new_file': new_file,
		'title': grade_title,
		'result': grade_result,
		'form' : form,
	}
	return render(request, 'tenant_grader/graderpage.html', context)

def getGradesFromDB(tenant_id):
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
        new_file_location = parseJavaFile(diagram_type, filename)
        uploaded_file_url = fs.url(filename)
    	return new_file_location
# USER = osp.join(osp.expanduser('~'), 'son')
# MEDIA = osp.join(os.getcwd(), 'media')
# STATIC = osp.join(os.getcwd(), 'static')
# JAR = osp.join(USER, 'class', 'umlparser.jar')
# CLASS = osp.join(USER, 'class', 'class')
# SEQ = osp.join(USER, 'seq', 'sequence')
# SEQ_MAKE = osp.join(USER, 'seq')
# OUTPUT = osp.join(USER, 'output')

def parseJavaFile(diagram_type, filename):
	if diagram_type == '1':
		# print filename
		# print CLASS
		# print MEDIA
		unzipFile(osp.join(MEDIA, filename), CLASS)
		sp.call(["java", "-jar", JAR, CLASS, osp.join(OUTPUT, 'output.png')])
	else:
		# print filename
		unzipFile(osp.join(MEDIA, filename), SEQ)
		sp.call(["make", "-C", SEQ_MAKE, 'demo'])
	timestr = time.strftime("%Y%m%d-%H%M%S")
	key = timestr+'.png'
	newfile = osp.join(STATIC, key)
	sp.call(["cp", osp.join(OUTPUT, 'output.png'), newfile])
	data = open(newfile, 'rb')
	s3 = boto3.resource('s3')
	s3.Bucket('javaparser').put_object(Key=key, Body=data)
	object_acl = s3.ObjectAcl('javaparser', key)
	response = object_acl.put(ACL='public-read')
	return key
		
def unzipFile(curdir, extractdir):
	print 'inside unzipfile'
	print curdir
	print extractdir
	sp.call(["unzip", "-j", curdir, '-d', extractdir])

	# zip_ref = zipfile.ZipFile(curdir, 'r')
	# zip_ref.extractall(extractdir)
	# zip_ref.close()

def cleanFile():
	sp.call(["make", "-C", SEQ_MAKE, 'clean'])
	sp.call(["rm", "-rf", MEDIA])
	sp.call(["mkdir", MEDIA])
	sp.call(["rm", "-rf", STATIC])
	sp.call(["mkdir", STATIC])
	sp.call(["rm", "-rf", CLASS])
	sp.call(["mkdir", CLASS])
	sp.call(["rm", "-rf", SEQ])
	sp.call(["mkdir", SEQ])
	sp.call(["rm", "-rf", OUTPUT])
	sp.call(["mkdir", OUTPUT])


