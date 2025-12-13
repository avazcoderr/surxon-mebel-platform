from rest_framework import serializers
from .models.categories import Category
from .models.products import Product


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "children")


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product list view"""
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ("id", "title", "description", "price", "category", "code", 
                 "discount_percentage", "discounted_price", "has_discount")


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product detail view with all required fields"""
    category = serializers.CharField(source='category.name', read_only=True)
    color_code = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ("id", "title", "description", "price", "color_code", "category", 
                 "code", "discount_percentage", "discounted_price", "has_discount", 
                 "created_at", "updated_at")
    
    def get_color_code(self, obj):
        """Return the first color code or None if no colors available"""
        if obj.color_codes and isinstance(obj.color_codes, list) and len(obj.color_codes) > 0:
            return obj.color_codes[0]
        return None
