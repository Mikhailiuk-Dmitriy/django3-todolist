from typing import Any

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Todo(models.Model):
    title: Any = models.CharField(max_length=100)
    memo: Any = models.TextField(blank=True)
    created: Any = models.DateTimeField(auto_now_add=True)
    datecompleted: Any = models.DateTimeField(blank=True, null=True)
    important: Any = models.BooleanField(default=False)
    user: Any = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"
