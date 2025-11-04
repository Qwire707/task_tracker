from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from tasks import models
from tasks import forms
from tasks.mixins import UserIsOwnerMixin


class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/tasks_list.html'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = forms.TaskFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset


class TasksCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'tasks/tasks_create.html'
    success_url = reverse_lazy("tasks-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TasksUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'tasks/tasks_update.html'
    success_url = reverse_lazy("tasks-list")


class TasksDetailView(DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'tasks/tasks_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm()
        context['comments'] = context['task'].comments.all()
        return context




    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect("tasks-detail", pk=comment.task.pk)
        else:
            pass



class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    template_name = 'tasks/tasks_delete.html'
    success_url = reverse_lazy("tasks-list")





    




