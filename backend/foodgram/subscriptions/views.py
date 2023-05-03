from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404

from api.serializer import SubscriptionSerializer
from users.models import CustomUser
from .models import Subscription


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        following = get_object_or_404(CustomUser, pk=kwargs['user_id'])
        request.data['user'] = request.user
        serializer = self.get_serializer(following, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



