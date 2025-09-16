from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Menu
from .serializers import MenuSerializer 


class MenuPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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