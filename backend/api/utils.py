from datetime import date

from django.http import HttpResponse


def generate_shopping_list_response(data):
    today = date.today().strftime("%d-%m-%Y")
    shopping_list = f'Список покупок на: {today}\n\n'
    for ingredient in data:
        shopping_list += (
            f'{ingredient["ingredients__name"]} '
            f'({ingredient["ingredients__measurement_unit"]}) — '
            f'{ingredient["amounts"]}\n'
        )
    file = HttpResponse(shopping_list,
                        content_type='text/plain; charset=utf-8')
    file['Content-Disposition'] = ('attachment; '
                                   'filename=shopping_list.txt')
    return file


def method_create(serializer, request, pk):
    request.data['recipe'] = pk
    request.data['user'] = request.user.id
    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data
