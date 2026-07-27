# library/urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .views import (
    RegisterView,
    UserDetailView,
    UserListView,
    AssignRoleView,
    BookListCreateView,
    BookDetailView,
)

urlpatterns = [
    # 1. POST /api/register/
    path('register/', RegisterView.as_view(), name='register'),

    # 2. POST /api/login/
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # 3. GET /api/me/
    path('me/', UserDetailView.as_view(), name='user_me'),

    # 4. GET /api/books/
    # 5. POST /api/books/
    path('books/', BookListCreateView.as_view(), name='book_list_create'),

    # 6. PUT /api/books/{id}/
    # 7. DELETE /api/books/{id}/
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),

    # 8. POST /api/users/{id}/assign-role/
    path('users/<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign_role'),

    # 9. GET /api/users/
    path('users/', UserListView.as_view(), name='user_list'),
]