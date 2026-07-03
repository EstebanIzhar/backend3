from rest_framework import viewsets
from .models import Platillo
from .serializers import PlatilloSerializer

class PlatilloViewSet(viewsets.ModelViewSet):
    queryset = Platillo.objects.all()
    serializer_class = PlatilloSerializer