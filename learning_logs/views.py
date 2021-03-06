# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def check_topic_user(request, topic):
	if topic.user != request.user:
		raise Http404

def index(request):
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	topics = Topic.objects.filter(user=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	topic = get_object_or_404(Topic, id=topic_id)
	check_topic_user(request,topic)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.user = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form':form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def edit_topic(request, topic_id):
	topic = get_object_or_404(Topic, id=topic_id)
	check_topic_user(request,topic)

	if request.method != 'POST':
		form = TopicForm(instance=topic)
	else:
		form = TopicForm(instance=topic, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'topic':topic, 'form': form}
	return render(request, 'learning_logs/edit_topic.html', context)

@login_required
def delete_topic(request, topic_id):
	topic = get_object_or_404(Topic, id=topic_id)
	check_topic_user(request, topic)

	topic.delete()
	return HttpResponseRedirect(reverse('learning_logs:topics'))

@login_required
def new_entry(request, topic_id):
	topic = get_object_or_404(Topic, id=topic_id)
	check_topic_user(request,topic)

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	entry = get_object_or_404(Entry, id=entry_id)
	topic = entry.topic
	check_topic_user(request,topic)

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

	context = {'entry': entry, 'topic':topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
	entry = get_object_or_404(Entry, id=entry_id)
	topic = entry.topic
	check_topic_user(request, topic)

	entry.delete()
	return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))