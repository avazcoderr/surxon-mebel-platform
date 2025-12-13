from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404

from .models.categories import Category
from .models.products import Product
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer
)
from utils.response_format import APIResponse
from utils.pagination import CustomPageNumberPagination


class CategoryListAPIView(generics.ListAPIView):
    """
    Returns all parent categories (those with no parent) and for each parent
    includes its child categories in the `children` list.

    URL (when included under `api/products/`): GET /api/products/categories/
    """
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(parent__isnull=True).prefetch_related("children")
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            data=serializer.data,
            message="Categories retrieved successfully"
        )


class ProductListAPIView(generics.ListAPIView):
    """
    Returns paginated list of all products.

    URL: GET /api/products/
    """
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.select_related("category", "brand").order_by("-created_at")
    serializer_class = ProductListSerializer
    pagination_class = CustomPageNumberPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Returns detailed information about a specific product.

    URL: GET /api/products/<uuid:product_id>/
    """
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.select_related("category", "brand")
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(
            data=serializer.data,
            message="Product details retrieved successfully"
        )


class ProductListByCategoryAPIView(generics.ListAPIView):
    """
    Returns paginated products under a specific category. Behavior:
    - If the category is a parent (no parent), return products from all its child categories.
    - If the category is a child (has a parent), return products from that category only.

    URL example (when included under `api/products/`):
      GET /api/products/categories/<uuid:category_id>/products/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductListSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)

        if category.is_parent:
            # Get all child category ids and return products belonging to them
            child_ids = category.children.values_list("id", flat=True)
            qs = Product.objects.filter(category_id__in=list(child_ids))
        else:
            # Child category: return products in this category only
            qs = Product.objects.filter(category=category)

        # optimize: bring related data in one query
        return qs.select_related("category", "brand").order_by("-created_at")


# View instances for URL patterns
category_list_view = CategoryListAPIView.as_view()
product_list_view = ProductListAPIView.as_view()
product_detail_view = ProductDetailAPIView.as_view()
product_list_by_category_view = ProductListByCategoryAPIView.as_view()