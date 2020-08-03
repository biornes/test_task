from django import forms


class ImageParams(forms.Form):
	width = forms.IntegerField(label = 'Ширина')
	height = forms.IntegerField(label = 'Высота')


class NewImage(forms.Form):
	link = forms.CharField(label = 'Cсылка')
	file = forms.CharField(label = 'Файл')