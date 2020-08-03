from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse
from .forms import ImageParams, NewImage

def index(request):
	data = {'header': 'Список изображений', 'padding': 'Нет доступных изображений', 'content': 'Добавить изображение'}
	return TemplateResponse(request, 'index.html', context = data)


def addImage(request):
	newImageForm = NewImage()
	# pass
	data = {'form': newImageForm, 'header': "Новое изображение"}
	return TemplateResponse(request, 'addImage.html', context = data)
	# return HttpResponse("<b>hello world<b>")
	# return HttpResponseRedirect(request, 'image.html')