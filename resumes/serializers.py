from rest_framework import serializers

from resumes.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    errorMessage = serializers.CharField(source="error_message")
    class Meta:
        model = Resume
        fields = ("id", "status", "errorMessage")
