from django.conf import settings
from django.db import models


class Task(models.Model):

    """
    Core data model for the Task Manager API.

    DESIGN DECISIONS:
        owner       → ForeignKey to AUTH_USER_MODEL (not a hardcoded User import)
                       because the custom user model lives in apps.users. Using
                       settings.AUTH_USER_MODEL keeps this decoupled.

        status      → TextChoices enum, not a BooleanField. Booleans only have
                       two states. Real workflows have at least three (todo,
                       in_progress, done) and often more. Enums are extendable
                       without a breaking migration.

        description → blank=True + default="" means the column is always a string,
                       never NULL. Consistent types reduce edge cases in serializers
                       and client code.

        due_date    → DateField (not DateTimeField) because deadlines are calendar
                       days, not moments in time. null=True + blank=True because
                       not every task has a deadline.

        created_at  → auto_now_add=True: set once on INSERT, never changeable.
        updated_at  → auto_now=True: updated automatically on every save().
                       Both are read_only in the serializer.

    FUTURE CONSIDERATIONS:
        - Add priority = TextChoices (low, medium, high, critical)
        - Add soft delete (is_deleted + deleted_at)
        - Add tags (ManyToManyField to a Tag model)
    """

    class Status(models.TextChoices):
        
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

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
        return f"[{self.status}] {self.title} (owner: {self.owner})"