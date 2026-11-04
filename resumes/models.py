from django.db import models


class Resume(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="resumes/%Y/%m/")
    error_message = models.TextField(blank=True)
    class Status(models.TextChoices):
        PENDING = "PENDING","Pending"
        DONE = "DONE","Done"
        PROCESSING = "PROCESSING", "Processing"
        FAILED = "FAILED","Failed"
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    def __str__(self):
        return f"Resume: Id{self.id} | File {self.file.name}"


class Candidate(models.Model):
    resume= models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    email = models.EmailField()
    birth_date = models.DateTimeField()