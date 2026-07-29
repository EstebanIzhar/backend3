from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Project, Task
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProjectSerializer,
    TaskSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        user_id = request.data.get("user_id")
        user = User.objects.get(pk=user_id)
        project.members.add(user)
        return Response(
            {
                "message": "Member added.",
                "project": ProjectSerializer(project).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def change_owner(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        owner = User.objects.get(
            pk=request.data.get("owner")
        )
        project.owner = owner
        project.save()
        return Response(
            ProjectSerializer(project).data
        )

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(
            pk=request.data.get("user_id")
        )
        task.assigned_to = user
        task.save()
        return Response(
            TaskSerializer(task).data
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        task.status = "completed"
        task.actual_hours = request.data.get(
            "actual_hours"
        )
        task.save()
        return Response(
            TaskSerializer(task).data
        )