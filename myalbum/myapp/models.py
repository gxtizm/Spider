from django.db import models
from datetime import datetime
# Create your models here.
class Album(models.Model):
	title=models.CharField(max_length=32)
	name=models.CharField(max_length=32)
	addtime=models.DateTimeField(default=datetime.now)
	filename =models.CharField(max_length=64)

	def __str__(self):
		return "%s"%(self.title)