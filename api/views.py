from django.http import JsonResponse
from api.serializers import ProductSerializer , OrderSerializer
from api.models import Product , Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many =True) #many add when more than one elements
   # return JsonResponse({
    # 'data' : serializer .data     ###normal django
   # })
    return Response(serializer.data) ### for DRF

@api_view(['GET'])
def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)   # single product
    serializer = ProductSerializer(product)
  
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many =True) #many add when more than one elements
   # return JsonResponse({
    # 'data' : serializer .data     ###normal django
   # })
    return Response(serializer.data) ### for DRF