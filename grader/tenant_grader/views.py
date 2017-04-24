# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from .models import TenantData, TenantFields, TenantTable
# Create your views here.
def grader(request):
	grade_title, grade_result = getGradesFromDB()

	print request.FILES
	file = uploadFile(request)

	context = {
		'uploaded_file_url': file,
		'title': grade_title,
		'result': grade_result
	}
	return render(request, 'tenant_grader/graderpage.html', context)

def getGradesFromDB(tenant_id='khwu'):
	field = TenantFields.objects.filter(tenant_id=tenant_id).order_by('field_column')
	grade_title = ['Record Number']
	for fi in field:
		grade_title.append(fi.field_name)
	grade_result = []
	data = TenantData.objects.filter(tenant_id=tenant_id).order_by('record_id')
	for da in data:
		temp = [da.record_id, da.column_1, da.column_2]
		grade_result.append(temp)
	return grade_title, grade_result

# reference: https://github.com/sibtc/simple-file-upload.git
def uploadFile(request):
    if request.method == 'POST' and request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
    	return "File uploaded"
    elif not request.FILES:
    	return "Please select a file"