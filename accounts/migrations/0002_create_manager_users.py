from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_manager_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    # Product Manager
    User.objects.create(
        name='Product',
        surname='Manager',
        email='product@manager.com',
        password=make_password('product123'),  # password is 'product123'
        role=1
    )
    # Sales Manager
    User.objects.create(
        name='Sales',
        surname='Manager',
        email='sales@manager.com',
        password=make_password('sales123'),  # password is 'sales123'
        role=2
    )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_manager_users),
    ]