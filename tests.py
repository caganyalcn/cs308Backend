from django.test import SimpleTestCase
from decimal import Decimal
from accounts.models import User
from address.models import Address
from products.models import Category, Product, Cart, CartItem
from orders.models import Order, OrderItem
from reviews.models import Review

class SimpleModelTests(SimpleTestCase):
    def test_user_str(self):
        u = User(name="A", surname="B", email="a@b.com", password="p")
        self.assertEqual(str(u), "a@b.com")

    def test_user_check_password_false(self):
        u = User(name="A", surname="B", email="a@b.com", password="p")
        self.assertFalse(u.check_password("p"))

    def test_user_is_admin_default_false(self):
        u = User(name="A", surname="B", email="a@b.com", password="p")
        self.assertFalse(u.is_admin)

    def test_user_has_email_field(self):
        self.assertTrue(hasattr(User, 'email'))

    def test_address_str(self):
        addr = Address(user=None, title="Home", line1="123", city="City", zip="000")
        self.assertEqual(str(addr), "Home - City")

    def test_address_has_city_field(self):
        self.assertTrue(hasattr(Address, 'city'))

    def test_product_str(self):
        p = Product(name="X", model=None, serial_number="SNX", description="D",
                    price=Decimal("1.23"), stock_quantity=1,
                    category="C", warranty_status=True,
                    distributor_info="Info", image_url="http://")
        self.assertEqual(str(p), "X")

    def test_product_fields(self):
        p = Product(name="X", model="M", serial_number="SN1", description="D",
                    price=Decimal("1.23"), stock_quantity=5,
                    category="C", warranty_status=False,
                    distributor_info="Info", image_url="")
        self.assertEqual(p.stock_quantity, 5)

    def test_product_model_blank_allowed(self):
        p = Product(name="X", model=None, serial_number="SN1", description="D",
                    price=Decimal("1"), stock_quantity=1,
                    category="C", warranty_status=False,
                    distributor_info="I", image_url="")
        self.assertIsNone(p.model)

    def test_product_has_price_field(self):
        self.assertTrue(hasattr(Product, 'price'))

    def test_cart_default_user(self):
        c = Cart()
        self.assertIsNone(c.user)

    def test_cart_has_created_at(self):
        self.assertTrue(hasattr(Cart, 'created_at'))

    def test_cartitem_default_quantity(self):
        ci = CartItem(cart=None, product=None)
        self.assertEqual(ci.quantity, 1)

    def test_cartitem_total_price(self):
        p = Product(name="X", model="M", serial_number="SNX", description="D",
                    price=Decimal("2.00"), stock_quantity=1,
                    category="C", warranty_status=False,
                    distributor_info="Info", image_url="")
        ci = CartItem(cart=None, product=p, quantity=3)
        self.assertEqual(ci.total_price(), Decimal("6.00"))

    def test_order_str(self):
        u = User(name="A", surname="B", email="a@b.com", password="p")
        o = Order(user=u, total_price=Decimal("10"), delivery_address="Addr")
        self.assertIn("a@b.com", str(o))

    def test_order_default_status(self):
        o = Order(user=None, total_price=Decimal("0"), delivery_address="")
        self.assertEqual(o.status, "processing")

    def test_order_has_delivery_address(self):
        self.assertTrue(hasattr(Order, 'delivery_address'))

    def test_orderitem_total_price(self):
        oi = OrderItem(order=None, product=None, quantity=2, price_at_purchase=Decimal("3.00"))
        self.assertEqual(oi.get_total_price(), Decimal("6.00"))

    def test_orderitem_has_price_field(self):
        self.assertTrue(hasattr(OrderItem, 'price_at_purchase'))

    def test_review_str(self):
        u = User(name="A", surname="B", email="a@b.com", password="p")
        p = Product(name="X", model="M", serial_number="SNX", description="D",
                    price=Decimal("1"), stock_quantity=1,
                    category="C", warranty_status=False,
                    distributor_info="Info", image_url="")
        r = Review(product=p, user=u, rating=5, comment="Good", approved=True)
        self.assertEqual(str(r), "a@b.com - X (5)")

    def test_review_default_approved(self):
        r = Review(product=None, user=None, rating=1, comment="Test")
        self.assertFalse(r.approved)

    def test_review_has_rating_field(self):
        self.assertTrue(hasattr(Review, 'rating'))

    def test_review_comment_none_allowed(self):
        r = Review(product=None, user=None, rating=1, comment=None)
        self.assertIsNone(r.comment)

    def test_review_created_at_initially_none(self):
        r = Review(product=None, user=None, rating=1, comment="")
        self.assertIsNone(r.created_at)

    def test_order_created_at_initially_none(self):
        o = Order(user=None, total_price=Decimal("0"), delivery_address="")
        self.assertIsNone(o.created_at)

    def test_user_email_unique_meta(self):
        # User.email alanı unique=True olmalı
        field = User._meta.get_field('email')
        self.assertTrue(field.unique)

    def test_user_name_max_length_meta(self):
        # User.name alanının max_length > 0
        field = User._meta.get_field('name')
        self.assertGreater(field.max_length, 0)

    def test_product_serial_number_unique_meta(self):
        # Product.serial_number unique=True olmalı
        field = Product._meta.get_field('serial_number')
        self.assertTrue(field.unique)

    def test_cartitem_quantity_default_meta(self):
        # CartItem.quantity default değeri 1 olmalı
        field = CartItem._meta.get_field('quantity')
        self.assertEqual(field.default, 1)

    def test_order_status_default_meta(self):
        # Order.status default olarak 'processing' atalı
        field = Order._meta.get_field('status')
        self.assertEqual(field.default, 'processing')
    
    def test_category_str(self):
        c = Category(name="Electronics", description="Devices")
        self.assertEqual(str(c), "Electronics")

    def test_category_has_description_field(self):
        self.assertTrue(hasattr(Category, 'description'))

    def test_category_created_at_exists(self):
        self.assertTrue(hasattr(Category, 'created_at'))

    def test_product_category_foreign_key(self):
        self.assertTrue(hasattr(Product, 'category'))

    def test_cart_has_user_field(self):
        self.assertTrue(hasattr(Cart, 'user'))

    def test_cart_has_items_relation(self):
        self.assertTrue(hasattr(Cart, 'items'))

    def test_cartitem_product_field(self):
        self.assertTrue(hasattr(CartItem, 'product'))

    def test_cartitem_cart_field(self):
        self.assertTrue(hasattr(CartItem, 'cart'))

    def test_user_role_default(self):
        u = User(name="A", surname="B", email="a@b.com", password="p")
        self.assertEqual(u.role, 0)

    def test_user_has_role_field(self):
        self.assertTrue(hasattr(User, 'role'))
    
    def test_address_user_relation(self):
        self.assertTrue(hasattr(Address, 'user'))

    def test_product_stock_quantity_field(self):
        self.assertTrue(hasattr(Product, 'stock_quantity'))

    def test_order_created_at_auto_add(self):
        self.assertTrue(hasattr(Order, 'created_at'))

    def test_order_has_user_foreign_key(self):
        self.assertTrue(hasattr(Order, 'user'))

    def test_orderitem_order_field(self):
        self.assertTrue(hasattr(OrderItem, 'order'))
