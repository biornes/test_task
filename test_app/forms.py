from django import forms


class ImageParams(forms.Form):
	width = forms.IntegerField(label = 'Ширина')
	height = forms.IntegerField(label = 'Высота')


class NewImage(forms.Form):
	fileLink = forms.CharField(label = 'Cсылка', required = False)
	fileLocal = forms.ImageField(label = 'Файл', required = False)
