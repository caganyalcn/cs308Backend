from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from accounts.authentication import CustomSessionAuthentication
from .permissions import IsSalesManager

@api_view(["GET"])
@authentication_classes([CustomSessionAuthentication])
@permission_classes([IsSalesManager])
def hello_sales(request):
    return Response({"msg": "Merhaba Satış Yöneticisi!"})
