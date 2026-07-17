from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):

        order = self.get_object()

        if not request.user.is_staff and order.user != request.user:
            raise PermissionDenied(
                "No tienes permiso para cancelar este pedido."
            )

        return self.destroy(request, *args, **kwargs)