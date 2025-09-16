from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Menu
from .serializers import MenuSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializers_class = MenuSerializer
    permissions_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error":str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )