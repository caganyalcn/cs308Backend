from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    ROLE_CHOICES = [
        (0, 'user'),
        (1, 'product_manager'),
        (2, 'sales_manager')
    ]
    
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    delivery_address = models.CharField(max_length=255, null=False, blank=False, default='Default Address')

    def save(self, *args, **kwargs):
        # Always hash the password on first save
        if self._state.adding:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the user's full name (name and surname).
        """
        full_name = f"{self.name} {self.surname}"
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the user's first name.
        """
        return self.name

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
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


