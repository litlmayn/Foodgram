from rest_framework import viewsets

from api.serializer import TegSerializer
from .models import Teg


class TegViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teg.objects.all()
    serializer_class = TegSerializer
