from django.db import models
from config.g_model import TimeStampMixin


# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    file_path = models.URLField(blank=True, null=True)
    img = models.ImageField(upload_to='product-image', blank=True, null=True)


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0, blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.variant_title + ' || ' + '|| product: ' + self.product.title


class ProductVariantPrice(TimeStampMixin):
    product_varients = models.ManyToManyField(ProductVariant)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
