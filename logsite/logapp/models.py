from django.db import models
from django.forms import ModelForm
from djangotoolbox.fields import EmbeddedModelField, ListField

class Log(models.Model):
	text = models.TextField()
	user = models.CharField(max_length=255)
	time = models.DateTimeField(auto_now_add=True)

class Log_wordcount(models.Model):
	word = models.CharField(max_length=255)
	value = models.IntegerField(default=0)

class Log_emote(models.Model):
	face = models.CharField(max_length=255)
	value = models.IntegerField(default=0)

class Log_populartimes(models.Model):
	prettyprint = models.CharField(max_length=255)
	hour = models.IntegerField(default=0)
	value = models.IntegerField(default=0)

class Log_popularity(models.Model):
	user = models.CharField(max_length=255)
	value = models.IntegerField(default=0)

class Log_network_summary(models.Model):
	talker = models.CharField(max_length=255)
	sumvalue = models.IntegerField(default=0)
	listener = ListField(EmbeddedModelField('Friends'))

class Friends(models.Model):
	user = models.CharField(max_length=255)
	value = models.IntegerField(default=0)

class Log_streams(models.Model):
	time = models.DateTimeField()
	streams = ListField(EmbeddedModelField('Streams'))

class Streams(models.Model):
	status = models.CharField(max_length=255)
	game = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	viewers = models.IntegerField(default=0)

class Log_wordline_count(models.Model):
	user = models.CharField(max_length=255)
	linecount = models.IntegerField(default=0)
	wordcount = models.IntegerField(default=0)

class Log_wordline_count_meta(models.Model):
	totalword = models.IntegerField(default=0)
	totalline = models.IntegerField(default=0)

class Log_wordline_std_meta(models.Model):
	avg = models.IntegerField(default=0)
	stddev = models.IntegerField(default=0)


'''
Logging error
ubuntu@ip-10-166-206-54:~/fourthtry/logsite$ python manage.py startapp logapp
/usr/local/lib/python2.7/dist-packages/django/conf/__init__.py:221: DeprecationWarning: You have no filters defined on the 'mail_admins' logging handler: adding implicit debug-false-only filter. See http://docs.djangoproject.com/en/dev/releases/1.4/#request-exceptions-are-now-always-logged DeprecationWarning)

Error rendering admins in mongodb
http://stackoverflow.com/questions/13138816/django-admin-filters-and-mongodb-caught-databaseerror-while-rendering-this-que

Admin site
http://www.djangobook.com/en/2.0/chapter06.html

General
https://code.djangoproject.com/wiki/Tutorials
http://django-mongodb-engine.readthedocs.org/en/latest/topics/setup.html
http://api.mongodb.org/python/current/tutorial.html
'''