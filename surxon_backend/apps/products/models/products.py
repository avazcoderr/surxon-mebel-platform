import string
import random
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from utils import AbstractBaseModel
from .categories import Category


class Product(AbstractBaseModel):
    """
    Product model that can only be linked to child categories.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # JSON field for multiple HEX color codes
    color_codes = models.JSONField(
        default=list,
        help_text="List of HEX color codes (e.g., ['#FF0000', '#00FF00', '#0000FF'])"
    )
    
    # Unique short code for each product
    code = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True,
        help_text="Auto-generated unique product code (e.g., 'MNK-0258')"
    )
    
    # Percentage-based discount
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text="Discount percentage (0-100)"
    )
    
    # Link to child category only
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        help_text="Must be a child category (not a parent category)"
    )

    # Brand association
    brand = models.ForeignKey(
        "brands.Brand",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        help_text="Optional link to the product's brand"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    def clean(self):
        """
        Validate that the product is only linked to child categories.
        """
        if self.category and self.category.is_parent:
            raise ValidationError({
                "category": "Products can only be linked to child categories."
            })
        
        # Validate color codes format
        if self.color_codes:
            if not isinstance(self.color_codes, list):
                raise ValidationError({
                    "color_codes": "Color codes must be a list of HEX color codes."
                })
            
            for color in self.color_codes:
                if not isinstance(color, str) or not color.startswith("#") or len(color) != 7:
                    raise ValidationError({
                        "color_codes": f"Invalid HEX color code: {color}. "
                                     "Use format #RRGGBB (e.g., #FF0000)"
                    })
                
                # Validate HEX characters
                try:
                    int(color[1:], 16)
                except ValueError:
                    raise ValidationError({
                        "color_codes": f"Invalid HEX color code: {color}. "
                                     "Contains non-hexadecimal characters."
                    })
    
    def save(self, *args, **kwargs):
        # Generate unique product code if not provided
        if not self.code:
            self.code = self._generate_unique_code()
        
        # Run validation
        self.clean()
        super().save(*args, **kwargs)
    
    def _generate_unique_code(self):
        """
        Generate a unique product code in format "ABC-1234"
        """
        while True:
            # Generate 3 random uppercase letters
            letters = "".join(random.choices(string.ascii_uppercase, k=3))
            # Generate 4 random digits
            digits = "".join(random.choices(string.digits, k=4))
            code = f"{letters}-{digits}"
            
            # Check if code is unique
            if not Product.objects.filter(code=code).exists():
                return code
    
    @property
    def discounted_price(self):
        """Calculate the price after applying discount"""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price
    
    @property
    def has_discount(self):
        """Returns True if product has a discount"""
        return self.discount_percentage > 0
