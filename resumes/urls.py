from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    # Resumes
    path("resumes/<int:pk>/", views.resume_detail, name="resume-detail"),
]
