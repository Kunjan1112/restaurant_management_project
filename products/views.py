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

def menu_view(request):  
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {"items":items})

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name' : item.name,
            'price' : float(item.price),
            'quantity' : 1
        }

    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item[quantity] for item in cart.values())
    return render(request, 'cart.html', {'cart':cart, 'total':total})

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('view_cart')