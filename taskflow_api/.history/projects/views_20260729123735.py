from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Project, Task
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProjectSerializer,
    TaskSerializer,
)
from .permissions import IsOwnerOrMember, IsTaskAssigneeOrProjectOwner

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()  # <-- AGREGADO AQUÍ
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(owner=user) | Project.objects.filter(members=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return Response({"detail": "No tienes permiso para agregar miembros."}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        project.members.add(user)
        return Response({"message": "Miembro agregado exitosamente."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def change_owner(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return Response({"detail": "Solo el dueño actual puede transferir la propiedad."}, status=status.HTTP_403_FORBIDDEN)
        
        new_owner_id = request.data.get("owner")
        new_owner = get_object_or_404(User, pk=new_owner_id)
        project.owner = new_owner
        project.save()
        return Response(ProjectSerializer(project).data, status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # <-- AGREGADO AQUÍ
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskAssigneeOrProjectOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(project__owner=user) | Task.objects.filter(assigned_to=user)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if task.project.owner != request.user:
            return Response({"detail": "Solo el dueño del proyecto puede asignar tareas."}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        task.assigned_to = user
        task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        actual_hours = request.data.get("actual_hours")
        
        if actual_hours is None or not str(actual_hours).isdigit():
            return Response({"error": "Debe proporcionar 'actual_hours' como un número entero válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = "completed"
        task.actual_hours = int(actual_hours)
        task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)