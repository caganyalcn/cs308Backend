"""from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from decimal import Decimal
from django.shortcuts import get_object_or_404
from accounts.authentication import CustomSessionAuthentication
from .permissions import IsSalesManager
from products.models import Product, Wishlist
from orders.models import Order, OrderItem      # varsayım: bu modeller mevcut
from .serializers import PriceSerializer, DiscountSerializer

@api_view(["PUT"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def set_price(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ser = PriceSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    product.price = ser.validated_data["price"]
    product.is_priced = True
    product.save(update_fields=["price", "is_priced"])
    return Response({"status": "price set", "product_id": product.id})

# 1. PDF endpoint
@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def invoices_pdf(request):
    # ... ReportLab kodu buraya ...
    return FileResponse(buffer, as_attachment=True, filename=filename)

# 2. Chart JSON endpoint
@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def revenue_chart(request):
    start = request.GET["start"]; end = request.GET["end"]
    orders = Order.objects.filter(created_at__date__range=[start, end])
    data = []
    for o in orders:
        data.append({"date": o.created_at.date().isoformat(),
                     "revenue": float(o.total_price),
                     "cost": float(o.items.aggregate(sum=Sum('product__cost_price'))['sum']),
                     "profit": float(o.total_price) - float(o.items.aggregate(sum=Sum('product__cost_price'))['sum'])})
    return Response(data)


@api_view(["POST"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def set_discount(request):
    ser = DiscountSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    ids, percent = ser.validated_data["product_ids"], ser.validated_data["percent"]

    products = Product.objects.filter(id__in=ids, is_priced=True)
    updated = 0
    for p in products:
        p.discount_percent = percent
        p.price = (p.price * Decimal(100 - percent) / Decimal(100)).quantize(Decimal("0.01"))
        p.save(update_fields=["discount_percent", "price"])
        updated += 1

    # İsteğe bağlı: Wish-list mail bildirimi
    # emails = Wishlist.objects.filter(product__in=products).values_list("user__email", flat=True)
    # send_mail(...)

    return Response({"updated": updated})


@api_view(["GET"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def invoices_between(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    qs = Order.objects.filter(created_at__date__range=[start, end])
    data = [{
        "id": o.id,
        "customer": o.user.email,
        "total": o.total_price,
        "date": o.created_at.date().isoformat()
    } for o in qs]
    return Response(data)


@api_view(["GET"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def revenue_report(request):
    start = request.GET["start"]; end = request.GET["end"]
    orders = Order.objects.filter(created_at__date__range=[start, end]).prefetch_related("items", "items__product")

    revenue = sum(o.total_price for o in orders)
    cost = Decimal(0)
    for o in orders:
        for item in o.items.all():                          # varsayım: OrderItem modeli
            cost += item.product.cost_price * item.quantity

    profit = revenue - cost
    return Response({
        "revenue": f"{revenue:.2f}",
        "cost": f"{cost:.2f}",
        "profit": f"{profit:.2f}"
    })



@api_view(["GET"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def hello_sales(request):
    return Response({"msg": "Merhaba Satış Yöneticisi!"})"""


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from django.http import FileResponse
from decimal import Decimal
from accounts.authentication import CustomSessionAuthentication
from accounts.permission import IsSalesManager
from products.models import Product, Wishlist
from orders.models import Order, OrderItem
from .serializers import PriceSerializer, DiscountSerializer

@api_view(['PUT'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def set_price(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return Response({'error': 'Product not found'}, status=404)
    serializer = PriceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product.price = serializer.validated_data['price']
    product.is_priced = True
    product.save(update_fields=['price', 'is_priced'])
    return Response({'status': 'price set', 'product_id': product.id})

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def invoices_pdf(request):
    # PDF oluşturma kodu...
    return FileResponse(buffer, as_attachment=True, filename='invoices.pdf')

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def revenue_chart(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    orders = Order.objects.filter(created_at__date__range=[start, end])
    data = []
    for o in orders:
        cost_sum = o.items.aggregate(total_cost=Sum('product__cost_price'))['total_cost'] or 0
        data.append({
            'date': o.created_at.date().isoformat(),
            'revenue': float(o.total_price),
            'cost': float(cost_sum),
            'profit': float(o.total_price) - float(cost_sum)
        })
    return Response(data)

@api_view(['POST'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def set_discount(request):
    serializer = DiscountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ids, percent = serializer.validated_data['product_ids'], serializer.validated_data['percent']
    products = Product.objects.filter(pk__in=ids, is_priced=True)
    for p in products:
        p.discount_percent = percent
        p.price = (p.price * (100 - percent) / 100).quantize(Decimal('0.01'))
        p.save(update_fields=['discount_percent', 'price'])
    return Response({'updated': products.count()})

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def invoices_between(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = Order.objects.filter(created_at__date__range=[start, end])
    data = [{'id': o.id, 'customer': o.user.email, 'total': float(o.total_price), 'date': o.created_at.date().isoformat()} for o in qs]
    return Response(data)

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def revenue_report(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    orders = Order.objects.filter(created_at__date__range=[start, end]).prefetch_related('items', 'items__product')
    revenue = sum(o.total_price for o in orders)
    cost = sum(item.product.cost_price * item.quantity for o in orders for item in o.items.all())
    profit = revenue - cost
    return Response({'revenue': f"{revenue:.2f}", 'cost': f"{cost:.2f}", 'profit': f"{profit:.2f}"})

@api_view(['GET'])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsAuthenticated, IsSalesManager])
def hello_sales(request):
    return Response({'msg': 'Merhaba Satış Yöneticisi!'})