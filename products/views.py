from rest_framework.decorators import api_view
from rest_framework.response import Response

# def menu_list(request):
#     menu_items = [
#         {'name': 'Margherita Pizza', 'description' : 'Classic cheese and tomato pizaa', 'price' : 299},
#         {'name': 'Veggie Burger', 'description' : 'Burger with fresh vegetables and cheese', 'price' : 199},
#         {'name': 'Pasta Alfredo', 'description' : 'Creamy Alfredo pasta with mushrooms', 'price' : 249},
#     ]

#     return render(request, 'products/menu_list.html', {'menu_items':menu_items})

@api_view(['GET'])
def menu_list_api(request):
    menu_items = [
        {'name': 'Margherita Pizza', 'description': 'Classic cheese and tomato pizza', 'price': 299},
        {'name': 'Veggie Burger', 'description': 'Burger with fresh vegetables and cheese', 'price': 199},
        {'name': 'Pasta Alfredo', 'description': 'Creamy Alfredo pasta with mushrooms', 'price':249},
    ]

    return Response(menu_items)