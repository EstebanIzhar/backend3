from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterViewSet, ProjectViewSet, TaskViewSet, obtain_auth_token

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("register", RegisterViewSet, basename="register")
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_auth_token, name="api_token_auth"),
]