from django.db import models
from accounts.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    warranty_status = models.BooleanField(default=False)
    distributor_info = models.TextField()
    image_url = models.URLField()
    avg_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    is_priced = models.BooleanField(default=False)
    discount_rate = models.PositiveIntegerField(default=0)  # 0–90 kontrolü API’de
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # For guests
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
    
@property
def discount_percent(self):
    return self.discount_rate

@discount_percent.setter
def discount_percent(self, value):
    self.discount_rate = value