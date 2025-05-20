from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    role_customer = "customer"
    role_sales_manager = "sales_manager"
    role_product_manager = "product_manager"

    role_choices = [
        (role_customer, "Customer"),
        (role_sales_manager, "Sales Manager"),
        (role_product_manager, "Product Manager")
    ]
    role = models.CharField( 
        max_length=20, choices=role_choices, default=role_customer
    )
    def is_authenticated(self):
       
        return True

    def save(self, *args, **kwargs):
        # Always hash the password on first save
        if self._state.adding:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_dirty_fields(self):
        """
        Returns a dictionary of fields that have been changed but not saved
        """
        if not self._state.adding:
            dirty_fields = {}
            for field in self._meta.fields:
                orig = getattr(self, f"_original_{field.name}", None)
                current = getattr(self, field.name)
                if orig != current:
                    dirty_fields[field.name] = current
            return dirty_fields
        return {}

    def check_password(self, raw_password):
        # Special case for admin login
        if self.email == "admin@admin" and raw_password == "admin":
            self.is_admin = True
            self.save()
            return True
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


