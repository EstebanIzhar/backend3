from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdmin


class ProductListCreateView(generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):

        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsAdmin()]