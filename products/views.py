from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Menu, MenuCategory, MenuItem
from .serializers import MenuSerializer, MenuCategorySerializer, MenuItemSerializer


# ----------------------------------------MenuPagination------------------------------------

class MenuPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# -----------------------------------MenuSearchViewSet---------------------------------------

class MenuSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permissions_classes = [permissions.AllowAny]
    pagination_class = MenuPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        query = request.query_params.get("q")

        if query:
            queryset = queryset.filter(name_icontains=query)

        page = self.pagination_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# ------------------------------------MenuItemPriceRangeView----------------------------------

class MenuItemPriceRangeView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        try:
            if min_price is not None:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            if max_price = is not None:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
        except ValueError:
            return MenuItem.objects.none()

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset = if None or not queryset.exists():
            return Response(
                {"error": "No menu items found or invalid price values."},
                status = status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)