from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):

    STATUS = (
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'