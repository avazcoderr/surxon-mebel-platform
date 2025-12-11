from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from utils import AbstractBaseModel


class Category(AbstractBaseModel):
    """
    Category model with hierarchical structure for parent/child relationships.
    Only child categories (those with a parent) can have products linked to them.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ["name", "parent"]
    
    def __str__(self):
        return self.name
    
    def clean(self):
        """
        Validate parent-child relationships:
        - A parent cannot link to another parent
        - A child cannot link to another child
        """
        if self.parent:
            # This will be a child category
            if self.parent.parent is not None:
                raise ValidationError({
                    "parent": "A child category cannot be linked to another child category. "
                             "Please select a parent category (one without a parent)."
                })
        else:
            # Check if any existing children would become invalid
            if self.pk and self.children.filter(parent__isnull=False).exists():
                raise ValidationError({
                    "parent": "This category has child categories and cannot be made a child itself."
                })
    
    def save(self, *args, **kwargs):
        # Generate slug from name if not provided
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Run validation
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def is_parent(self):
        """Returns True if this is a parent category (no parent)"""
        return self.parent is None
    
    @property
    def is_child(self):
        """Returns True if this is a child category (has a parent)"""
        return self.parent is not None
    
    def get_full_name(self):
        """Returns the full category path (Parent > Child)"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name