from django.db import models

# Create your models here.
class Images(models.Model):
	path = models.CharField(max_length = 300)