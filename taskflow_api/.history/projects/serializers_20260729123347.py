from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Project, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"] # <-- Sin password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        # Cifra la contraseña correctamente usando create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "members", "created_at", "updated_at"]
        # Se omiten internal_notes y budget para usuarios comunes o se controlan por contexto

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "project", "assigned_to", 
            "status", "estimated_hours", "actual_hours", "created_at", "updated_at"
        ]
        # Se omite confidential_comment de la vista pública