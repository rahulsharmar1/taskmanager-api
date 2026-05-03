from django.db import models

# Create your models here.

class Task(models.Model):

    class Status(models.TextChoices):
        
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]   # newest tasks first by default
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"[{self.status}] {self.title}"