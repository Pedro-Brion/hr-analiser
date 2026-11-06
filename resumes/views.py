from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from resumes.models import Resume
from resumes.serializers import ResumeSerializer


def health(request):
    return JsonResponse({"status": "ok"})


@api_view(["GET"])
def resume_detail(request, pk):
    print(f"Fetching resume of id {pk}")
    r = get_object_or_404(Resume, pk=pk)
    return Response(ResumeSerializer(r).data)
