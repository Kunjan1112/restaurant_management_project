from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Menu
from .serializers import MenuSerializer

class MenuByCategoryView(ListAPIView):
    serializers_class = MenuSerializer
    permissions_classes = [AllowAny]

    def get_queryset(self):
        queryset = Menu.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_name_iexact=category)
        return queryset