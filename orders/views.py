from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Order
from .serializers import OrderSummarySerializer

# Create your views here.

# --------------------------------------------Order_Confirmation---------------------------

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {"order":order})

# ------------------------------------------------Thank_You------------------------------------

def thank_you(request):
        return render(request, 'order/thank_you.html')

# -------------------------------------------------OrderSummarySerializer-----------------------------

class OrderSummarySerializer(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSummarySerializer

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)