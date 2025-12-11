from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent", "is_parent", "is_child", "created_at"]
    list_filter = ["parent", "created_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created_at", "updated_at"]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("parent")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "category", "price", "discount_percentage", "discounted_price", "created_at"]
    list_filter = ["category", "discount_percentage", "created_at"]
    search_fields = ["title", "code", "description"]
    readonly_fields = ["id", "code", "created_at", "updated_at", "discounted_price"]
    
    fieldsets = (
        (None, {
            "fields": ("title", "description", "category")
        }),
        ("Pricing", {
            "fields": ("price", "discount_percentage", "discounted_price")
        }),
        ("Product Details", {
            "fields": ("code", "color_codes")
        }),
        ("Timestamps", {
            "fields": ("id", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "category__parent")
