from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Resume(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="resumes/%Y/%m/")
    error_message = models.TextField(blank=True)

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        DONE = "DONE", "Done"
        PROCESSING = "PROCESSING", "Processing"
        FAILED = "FAILED", "Failed"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return f"Resume: Id{self.id} | File {self.file.name}"


class Candidate(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    birth_date = models.DateField(null=True, blank=True)
    def __str__(self):
            return f"Candidate {self.name}: Resume Id{self.resume_id}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=150)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    technologies = models.JSONField(default=list)
    def __str__(self):
        return f"Experience in {self.company}: Resume Id{self.resume_id}"
    
class StackItem(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE, related_name="stack")
    name = models.CharField(max_length=100)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    def __str__(self):
        return f"{self.name} for {self.experience_years}years: {self.score}/5"
    
