from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.decorators import action

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
    try:
        order = Order.objects.get(id=order_id)
        result = send_order_confirmation_email(
            order_id=order.id,
            customer_email = order.customer.email,
            customer_name = order.customer.username,
            total_amount = order.total_amount
        )
        print(result)
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} not found.")

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['delete'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        try:
            order = self.get_object()

            if order.customer != request.user:
                return Response(
                    {"error":"You cannot cancel someone else's order."},
                    status = status.HTTP_403_FORBIDDEN,
                )

            order.status = "Cancelled"
            order.save()

            return Response(
                {"message": f"Order #{order.id} has been cancelled successfully. "},
                status = status.HTTP_200_OK,
            )

        except Order.DoesNotExist:
            return Response(
                {"error":"Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
