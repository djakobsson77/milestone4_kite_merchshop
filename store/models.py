from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ("tshirt", "T-shirts"),
        ("longsleeve", "Longsleeve & Hoodies"),
        ("poster", "Posters"),
        ("vinyl", "Vinyl & Special Editions"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True)

    def __str__(self):
        return self.name