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
	# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	if source.endswith(".png"):
		img = Image.open(source)
		img = img.convert('RGBA')
		source = source.replace('png', 'jpg')
		img.save(source, 'png')
	# source = BASE_DIR+source
	img = Image.open(source)
	output = source.replace('.jpg', str(size[0]) +'x' + str(size[1])) + ".jpg"
	# width, height = source.size
	resizedImage = img.resize(size)
	resizedImage.save(output)
	print (output)
	return output

def getImage(url):
	response = requests.get(url, stream=True)
	# print (response.raw)
	name = str(hash(datetime.now())) + '.jpg'
	with open("static/" + name, 'wb') as out_file:
		for chunk in response.iter_content(8192):
			# print (1)
			out_file.write(chunk)
		# shutil.copyfileobj(response.raw, out_file)
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
		# pass
		return TemplateResponse(request, 'addImage.html', context = data)
	elif request.method == 'POST':
		alertFlagEmpty = request.POST.get('fileLink') == None and request.FILES.get('fileLocal') == None
		alertFlagNotEmpty = (request.POST.get('fileLink') != None and request.POST.get('fileLink') != '') and request.FILES.get('fileLocal') != None
		print (alertFlagEmpty, alertFlagNotEmpty, request.POST.get('fileLink'), request.FILES.get('fileLocal'))
		print(request.POST.get('fileLink'))
		if alertFlagEmpty or alertFlagNotEmpty:
			print ('alert')
			return TemplateResponse(request, 'addImage.html', context = data)
		if request.POST.get('fileLink') not in (None, ''):
			imageName = getImage(request.POST.get('fileLink'))
		# print (image.name)
		# def handle_uploaded_file(f):
		elif request.FILES.get('fileLocal') != None:
			image = request.FILES.get('fileLocal')
			# help(image)
			imageName = image.name
			with open('static/' + image.name, 'wb') as out_file:
				for chunk in image.chunks():
					out_file.write(chunk)
		# image.save()
		imageDB = Images.objects.create(path = imageName)
		imageDB.save()
		# imageDB.path = 
		# return TemplateResponse(request, 'addImage.html')
		# return HttpResponseRedirect('/imageParams')
		# print ('11111', imageName)
		return HttpResponseRedirect('/imageParams/' + imageName)
		
def imageParams(request, imagename = '1'):
	paramsForm = ImageParams()
	src = imagename
	print (imagename)
	data = {'form': paramsForm, 'header': 'Image.jpg'}
	data['src'] = "/static/" + imagename

	if request.method == 'GET':
		return TemplateResponse(request, 'image.html', context = data)
	elif request.method == 'POST':
		src = imagename
		width = request.POST.get('width')
		height = request.POST.get('height')
		# data['src'] = src
		pathToImage = resizeImage('static/'+src, [int(width), int(height)])
		pathToImage = pathToImage.replace('static/', '')
		imageDB = Images.objects.get(path = imagename)
		imageDB.path = pathToImage
		imageDB.save()
		data['width'] = width
		data['height'] = height
		return HttpResponseRedirect('/imageParams/' + pathToImage)
		# return TemplateResponse(request, 'image.html', context = data)