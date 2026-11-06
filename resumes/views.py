from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from resumes.models import Resume


def health(request):
    return JsonResponse({"status": "ok"})


def resume_detail(request, pk):
    print(f"Fetching resume of id {pk}")
    r = get_object_or_404(Resume, pk=pk)
    return JsonResponse(
        {
            "id": r.pk,
            "status": r.status,
            "errorMessage": r.error_message,
        }
    )
