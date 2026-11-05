from django.contrib import admin

from .models import Candidate, Experience, Resume, StackItem

MODELS = [Candidate, Experience, Resume, StackItem]

admin.site.register(MODELS)
