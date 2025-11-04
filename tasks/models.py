from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "TO DO"),
        ("in progress", "IN PROGRESS"),
        ("done", "DONE")
    ]
    PRIORITY_CHOICES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH")
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="todo")
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, default="low")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=200)
    media = models.FileField(upload_to='media_comments', null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} commented on {self.task}"