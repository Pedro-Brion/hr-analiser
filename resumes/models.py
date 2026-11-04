from django.db import models


class Resume(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.CharField(max_length=300)
    error_message = models.CharField(max_length=300)
    class Status(models.TextChoices):
        PENDING = "PENDING","Pending"
        DONE = "DONE","Done"
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    def __str__(self):
        return f"Resume: Id{self.id} | File {self.file.split("/")[-1]}"
