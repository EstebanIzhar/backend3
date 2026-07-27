from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'roles']

    def get_roles(self, obj):
        return list(obj.groups.values_list('name', flat=True))


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        # El primer usuario registrado es ADMIN; los siguientes son CLIENTE
        if User.objects.count() == 1:
            role_name = "ADMIN"
        else:
            role_name = "CLIENTE"

        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)
        return user


class AssignRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['ADMIN', 'BIBLIOTECARIO', 'CLIENTE'])

    def save(self, user):
        role_name = self.validated_data['role']
        # Limpia roles previos y asigna el nuevo
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'