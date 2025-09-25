from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action

from orders.models import Order

from orders.serializers import OrderSerializers, OrderStatusUpdateSerializer, OrderStatusSerializer

from utils.email_utils import send_order_confirmation_email

# -----------------------------------------OrderHistroyView--------------------------------------------------

class OrderHistroyView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# --------------------------------------------OrderViewSet----------------------------------------

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

# -------------------------------------------OrderCreateView-------------------------------------

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# --------------------------------------------UpdateOrderStatusView--------------------------------------

class UpdateOrderStatusView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            new_status = serializer.validated_data['status']


            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response(
                    {"error":"Order not found."},
                    status = http_status.HTTP_404_NOT_FOUND
                    )

            order.status = new_status
            order.save()

            return Response(
                {"message":"Order status update successfully.", "order_id": order.id, "new_status":order.status},
                status=http_status.HTTP_200_OK
            )

        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

# -------------------------------------------OrderStatusRetrieveAPIView---------------------------------------

class OrderStatusRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OrderStatusSerializer
    lookuo_field = 'unique_id'

    def get_queryset(self):
        return Order.objects.all()

    def get(self, request, *args, **kwargs):
        unique_id = self.kwargs.get('unique_id')
        try:
            order = self.get_queryset().get(unique_id=unique_id)
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"error": f"No Order found with ID {unique_id}"},
                status = status.HTTP_404_NOT_FOUND
            )

# -----------------------------------UserOrderHistoryView---------------------------------

class UserOrderHistoryView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except DatabaseError:
            return Response(
                {"error": "A database error occurred. Please try again later."}
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )