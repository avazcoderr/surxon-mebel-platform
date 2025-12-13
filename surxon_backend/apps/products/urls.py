from .views import (
    category_list_view, 
    product_list_view,
    product_detail_view,
    product_list_by_category_view as product_filter_view
)
from django.urls import path

urlpatterns = [
    path("", product_list_view, name="product-list"),
    path("<uuid:product_id>/", product_detail_view, name="product-detail"),
    path("categories/", category_list_view, name="category-list"),
    path("categories/<uuid:category_id>/products/", product_filter_view, name="product-list-by-category")
]