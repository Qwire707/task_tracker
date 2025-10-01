from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from tasks import models

class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/tasks_list.html'
    ordering = ['-created_at']
    




