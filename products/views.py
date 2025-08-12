from django.shortcuts import render

def menu_list(request):
    menu_items = [
        {'name': 'Margherita Pizza', 'description' : 'Classic cheese and tomato pizaa', 'price' : 299},
        {'name': 'Veggie Burger', 'description' : 'Burger with fresh vegetables and cheese', 'price' : 199},
        {'name': 'Pasta Alfredo', 'description' : 'Creamy Alfredo pasta with mushrooms', 'price' : 249},
    ]

    return render(request, 'products/menu_list.html', {'menu_items':menu_items})