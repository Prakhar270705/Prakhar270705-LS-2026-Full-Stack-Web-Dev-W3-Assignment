from django.core.cache import cache
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Bounty
from .permissions import IsOwner
from .serializers import RegisterSerializer, BountySerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


def bounty_cache_key(user_id):
    return f'bounties_list_{user_id}'


class BountyListCreateView(generics.ListCreateAPIView):
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bounty.objects.filter(owner=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        key = bounty_cache_key(request.user.id)
        cached_data = cache.get(key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, timeout=60)
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        cache.delete(bounty_cache_key(self.request.user.id))


class BountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Bounty.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(bounty_cache_key(self.request.user.id))

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(bounty_cache_key(self.request.user.id))
