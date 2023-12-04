from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    middle_name = models.CharField(max_length=120, blank=True)
    department = models.CharField(max_length=240, blank=True)
    job_title = models.CharField(max_length=240, blank=True)

    # def make_friends(self, other):
    #     self.friends.add(other)
    #     self.save()
    #     other.friends.add(self)
    #     other.save()

class Document(models.Model):
    STATUS_DOCUMENT_CHOICES = [
        ("Wait_Processing", "Ожидает обработки"),
        ("Wait_Fix", "Ожидает исправления"),
        ("Rejected", "Отклонен"),
        ("Complete", "Завершен"),
    ]

    name = models.CharField(max_length=120, blank=True)
    file = models.FileField(upload_to="documents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=120, choices=STATUS_DOCUMENT_CHOICES)
    need_sign = models.BooleanField(default=False)

    creator = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='sent_documents'
    )
    recipient = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='inbox_documents'
    )

class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="signatures")
    creator = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name='signatures'
    )
    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name='signatures'
    )