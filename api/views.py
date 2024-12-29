from django.db.models import Max
from django.http import JsonResponse
from api.serializers import ProductSerializer , OrderSerializer , ProductInfoSerializer
from api.models import Product , Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

#@api_view(['GET'])
#def product_list(request):
#    products = Product.objects.all()
#    serializer = ProductSerializer(products, many =True) #many add when more than one elements
   # return JsonResponse({
    # 'data' : serializer .data     ###normal django
   # })
#    return Response(serializer.data) ### for DRF
class ProductListAPIView(generics.ListAPIView):
    #queryset = Product.objects.all()
    #queryset = Product.objects.filter(stock__gt=0) # this will show only product which have  stock
    queryset = Product.objects.exclude(stock__gt=0) # this will show only product which have zero stock
    serializer_class = ProductSerializer




#@api_view(['GET'])
#def product_detail(request,pk):
  #  product = get_object_or_404(Product,pk=pk)   # single product
    #serializer = ProductSerializer(product)
  
   # return Response(serializer.data)
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer
    
    
    
"""

@api_view(['GET'])
def order_list(request):
    #orders = Order.objects.all() # 19 quries
    orders = Order.objects.prefetch_related('items__product' )  # 3 queries
    serializer = OrderSerializer(orders, many =True) #many add when more than one elements
   # return JsonResponse({
    # 'data' : serializer .data     ###normal django
   # })
    return Response(serializer.data) ### for DRF


""" 
class OrderListAPIView(generics.ListAPIView):
    
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
   
        qs=super().get_queryset()
            
        
        return qs.filter(user=self.request.user)
    
    
    
    
@api_view(['GET'])
def product_info(request):
    products= Product.objects.all()
    serializer = ProductInfoSerializer({
        'products' : products ,
        'count' : len(products) ,
        'max_price' : products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)