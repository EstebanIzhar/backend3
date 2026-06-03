from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor que 0."
            )
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo."
            )
        return value

    def validate_description(self, value):

        palabras_prohibidas = [
            "pirata",
            "ilegal",
            "gratis"
        ]

        for palabra in palabras_prohibidas:
            if palabra.lower() in value.lower():
                raise serializers.ValidationError(
                    f"Palabra prohibida encontrada: {palabra}"
                )

        return value

    def validate(self, data):

        if Product.objects.filter(
            name=data['name'],
            category=data['category']
        ).exists():

            raise serializers.ValidationError({
                "name": "Ya existe un producto con ese nombre en esta categoría."
            })

        return data