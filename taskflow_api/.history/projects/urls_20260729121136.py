from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterViewSet, ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("register", RegisterViewSet)
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
]