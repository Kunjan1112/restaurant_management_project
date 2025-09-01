from django.shortcuts import render

# Create your views here.

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {"order":order})

def thank_you(request):
        return render(request, 'order/thank_you.html')