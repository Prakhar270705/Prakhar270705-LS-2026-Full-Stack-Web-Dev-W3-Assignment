from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Bounty


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class BountySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    reward = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Bounty
        fields = ['id', 'target_name', 'reward', 'status', 'location', 'danger_level', 'owner', 'created_at']
