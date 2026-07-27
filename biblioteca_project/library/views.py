# library/views.py

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Book
from .serializers import (
    BookSerializer, 
    UserSerializer, 
    RegisterSerializer, 
    AssignRoleSerializer
)
from .permissions import IsAdmin, BookPermission

# POST /api/register/
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# GET /api/me/
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# GET /api/users/
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

# POST /api/users/{id}/assign-role/
class AssignRoleView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({
                'message': f'Rol {serializer.validated_data["role"]} asignado correctamente a {user.username}'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /api/books/ y POST /api/books/
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermission]

# PUT /api/books/{id}/ y DELETE /api/books/{id}/
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermission]