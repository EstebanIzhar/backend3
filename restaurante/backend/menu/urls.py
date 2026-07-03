from rest_framework.routers import DefaultRouter
from .views import PlatilloViewSet

router = DefaultRouter()
router.register(r'platillos', PlatilloViewSet)

urlpatterns = router.urls