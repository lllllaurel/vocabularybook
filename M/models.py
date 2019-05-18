from django.db import models

# Create your models here.
class UserMain(models.Model):
	username = models.CharField(max_length = 50)
	password = models.CharField(max_length = 50)
	date = models.DateTimeField()

class WordsMatch(models.Model):
	username = models.CharField(max_length = 50)
	english = models.TextField()
	chinese = models.TextField()
	total = models.TextField(default=0)
	errorrate = models.TextField(default=0)
	wordid = models.TextField(default=0)
	process_tag = models.SmallIntegerField(default=0)
	date = models.DateTimeField()

class Bugs(models.Model):
	username = models.CharField(max_length = 50)
	bugs = models.TextField(default=0)
	date = models.DateTimeField()