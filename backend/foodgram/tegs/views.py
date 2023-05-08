from rest_framework import viewsets

from api.serializer import TagSerializer
from .models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
