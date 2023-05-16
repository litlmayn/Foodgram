from datetime import date

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import response


def generate_shopping_list_response(data):
    today = date.today().strftime("%d-%m-%Y")
    shopping_list = f'Список покупок на: {today}\n\n'
    filename = 'shopping_list.txt'
    response['Content-Disposition'] = (f'attachment; '
                                       f'filename={filename}')
    for ingredient in data:
        shopping_list += (
            f'{ingredient["ingredients__name"]} '
            f'({ingredient["ingredients__measurement_unit"]}) — '
            f'{ingredient["amounts"]}\n'
        )
    return HttpResponse(shopping_list,
                        content_type='text/plain; charset=utf-8')


def method_create(serializer, request, pk):
    request.data['recipe'] = pk
    request.data['user'] = request.user.id
    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def method_delete(model, request, pk):
    get_object_or_404(model, user=request.user.id, recipe=pk).delete()
