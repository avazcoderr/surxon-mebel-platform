from django.db import models
from django.core.validators import FileExtensionValidator
from utils import AbstractBaseModel


class Brand(AbstractBaseModel):
    """
    Brand model represents a product brand with a name and an optional logo.
    """
    name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to="brands/logos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name
