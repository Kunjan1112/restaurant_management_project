from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializers
from utils.email_utils import send_order_confirmation_email

class OrderHistroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data)

def confirm_order(order_id):
    order = Order.objects.get(id=order_id)
    result = send_order_confirmation_email(
        order_id=order.id,
        customer_email = order.customer.email,
        customer_name = order.customer.username,
        total_amount = order.total_amount
    )

    print(result)