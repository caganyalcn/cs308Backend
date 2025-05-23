from django.db import models
from accounts.models import User
from django.utils import timezone
import hashlib
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Can be null as it will be set by sales manager
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    warranty_status = models.BooleanField(default=False)
    distributor_info = models.TextField()
    image_url = models.URLField()
    avg_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # For guests
    created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} favorites {self.product}"

# Helper function for hashing with a salt
def hash_with_salt(text, salt=None):
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt)
    hashed_text = hashlib.pbkdf2_hmac('sha256', text.encode('utf-8'), salt, 100000)
    return hashed_text.hex(), salt.hex()

# Not strictly needed for verification in this request, but useful
def check_hashed_text(text, hashed_text_hex, salt_hex):
    hashed_text_check, _ = hash_with_salt(text, salt_hex)
    return hashed_text_check == hashed_text_hex

# CreditCard model for storing hashed card details
class CreditCard(models.Model):
    # Assuming accounts.models.User is your User model
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='credit_cards')
    card_number_hash = models.CharField(max_length=64) # SHA-256 hash is 64 chars
    card_number_salt = models.CharField(max_length=32) # Salt as hex
    cvv_hash = models.CharField(max_length=64)
    cvv_salt = models.CharField(max_length=32)
    expiry_date = models.CharField(max_length=5) # MM/YY format (e.g., 12/25)
    card_holder_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Indicate card for the user, as number is hashed
        # In a real application, you might store last 4 digits separately for display
        return f"Card for {self.user.username if self.user else 'Guest'}"

    # Method to set card details with hashing
    def set_card_details(self, card_number, cvv):
        self.card_number_hash, self.card_number_salt = hash_with_salt(card_number)
        self.cvv_hash, self.cvv_salt = hash_with_salt(cvv)
