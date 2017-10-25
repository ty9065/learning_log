# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	user = models.ForeignKey(User)
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text
		
class Entry(models.Model):
	topic = models.ForeignKey(Topic)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'
			
	def __unicode__(self):
		if len(self.text)>50:
			return self.text[:50] + "..."
		else:
			return self.text
		