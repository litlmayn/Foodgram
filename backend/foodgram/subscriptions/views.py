from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, mixins
from django.shortcuts import get_object_or_404

from .models import Subscription
from api.serializer import SubscriptionSerializer
from users import models, views


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, **kwargs):
        following = get_object_or_404(models.CustomUser, pk=kwargs['user_id'])
        request.data['user'] = request.user.id
        request.data['following'] = following.id
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        following = get_object_or_404(models.CustomUser, pk=kwargs['user_id'])
        Subscription.objects.filter(following=following, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
