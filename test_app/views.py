from django.shortcuts import render, redirect
from django.urls import reverse
from PIL import Image
import requests
import os
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse
from .forms import ImageParams, NewImage
from .models import Images
from datetime import datetime

def resizeImage(source, size):
	img = Image.open(source)
	output = source.replace('.jpg', '_' + str(size[0]) +'x' + str(size[1])) + ".jpg"
	resizedImage = img.resize(size)
	resizedImage.save(output)
	return output

def getImage(url):
	response = requests.get(url, stream=True)
	name = str(hash(datetime.now())) + '.jpg'
	with open("static/" + name, 'wb') as out_file:
		for chunk in response.iter_content(8192):
			out_file.write(chunk)
	return name

def index(request):
	data = {'header': 'Список изображений',
	        'padding': 'Нет доступных изображений',
	        'content': 'Добавить изображение',
	        'db': Images.objects.all()
	        }
	return TemplateResponse(request, 'index.html', context = data)


def addImage(request):
	newImageForm = NewImage()
	data = {'form': newImageForm, 'header': "Новое изображение"}
	if request.method == 'GET':
		return TemplateResponse(request, 'addImage.html', context = data)
	elif request.method == 'POST':
		fileLinkData = request.POST.get('fileLink')
		fileLocalData = request.FILES.get('fileLocal')
		alertFlagEmpty = fileLinkData == None and fileLocalData == None
		alertFlagNotEmpty = fileLinkData not in (None, '') and fileLocalData != None
		if alertFlagEmpty or alertFlagNotEmpty:
			return TemplateResponse(request, 'addImage.html', context = data)
		if fileLinkData not in (None, ''):
			imageName = getImage(fileLocalData)
		elif fileLocalData != None:
			image = request.FILES.get('fileLocal')
			imageName = image.name
			with open('static/' + image.name, 'wb') as out_file:
				for chunk in image.chunks():
					out_file.write(chunk)
		imageDB = Images.objects.create(path = imageName)
		imageDB.save()
		return HttpResponseRedirect('/imageParams/' + imageName)
		
def imageParams(request, imageName):
	paramsForm = ImageParams()
	data = {'form': paramsForm, 'header': imageName}
	data['src'] = "/static/" + imageName
	if request.method == 'GET':
		return TemplateResponse(request, 'image.html', context = data)
	elif request.method == 'POST':
		width = request.POST.get('width')
		height = request.POST.get('height')
		pathToImage = resizeImage('static/' + imageName, [int(width), int(height)])
		pathToImage = pathToImage.replace('static/', '')
		imageDB = Images.objects.get(path = imageName)
		imageDB.path = pathToImage
		imageDB.save()
		return HttpResponseRedirect('/imageParams/' + pathToImage)
