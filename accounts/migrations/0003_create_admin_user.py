from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    # Check if admin user exists
    if not User.objects.filter(email='admin@admin').exists():
        # Create admin user with hashed password
        User.objects.create(
            name='Admin',
            surname='User',
            email='admin@admin',
            password=make_password('admin'),  # Hash the password
            is_admin=True
        )

def reverse_admin_user(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    # Delete admin user if it exists
    User.objects.filter(email='admin@admin').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_add_is_admin_field'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, reverse_admin_user),
    ] 