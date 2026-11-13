from rest_framework import serializers

from resumes.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    errorMessage = serializers.CharField(source="error_message")

    class Meta:
        model = Resume
        fields = ("id", "status", "errorMessage")
        read_only_fields = ("id", "status", "errorMessage")


class ResumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("file",)
    
    def validate_file(self,value):
        print(value)
