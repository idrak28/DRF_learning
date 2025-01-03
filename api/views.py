from django.db.models import Max
from django.http import JsonResponse
from api.serializers import ProductSerializer , OrderSerializer , ProductInfoSerializer
from api.models import Product , Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated ,IsAdminUser ,AllowAny
from rest_framework.views import APIView

from api.filters import ProductFilter ,InstockFilterBaackend

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination


##################################### both create and list view ######################################
class ProductListCreateAPIView(generics.ListCreateAPIView):
    
    queryset=Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    
    #filterset_fields = ['name', 'price']
    filterset_class = ProductFilter
    filter_backends =[
        DjangoFilterBackend, # django filter.py
        filters.SearchFilter,   #?search=coffe
        filters.OrderingFilter , #?ordering=price
        InstockFilterBaackend
        ]
    search_fields = ['name' , 'description']
    ordering_fileds = [ 'name' , 'price']
    
    #override pagination
   # pagination_class =PageNumberPagination
   # pagination_class.page_size =2
   # pagination_class.page_query_param='page_num'
  #  pagination_class.page_size_query_param='size'
   # pagination_class.max_page_size=5
    pagination_class =LimitOffsetPagination
    
    def get_permissions(self):
        self.permission_classes =[AllowAny]
        if self.request.method=="POST":
            self.permission_classes =[IsAdminUser]
        return super().get_permissions()

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    #queryset = Product.objects.filter(stock__gt=0) # this will show only product which have  stock
    #queryset = Product.objects.exclude(stock__gt=0) # this will show only product which have zero stock
    serializer_class = ProductSerializer
    
    
#@api_view(['GET'])
#def product_list(request):
#    products = Product.objects.all()
#    serializer = ProductSerializer(products, many =True) #many add when more than one elements
   # return JsonResponse({
    # 'data' : serializer .data     ###normal django
   # })
#    return Response(serializer.data) ### for DRF


class ProductCreateAPIView(generics.CreateAPIView):
    model=Product
    
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        
        return super().create(request,*args,**kwargs)
#######################################################################################################

#@api_view(['GET'])
#def product_detail(request,pk):
  #  product = get_object_or_404(Product,pk=pk)   # single product
    #serializer = ProductSerializer(product)
  
   # return Response(serializer.data)
#class ProductDetailAPIView(generics.RetrieveAPIView):
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
    def get_permissions(self):
        self.permission_classes =[AllowAny]
        if self.request.method in ['PUT' , 'PATCH' , 'DELETE']:
            self.permission_classes =[IsAdminUser]
        return super().get_permissions()

#########################################################################################################  
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

 #############################################################################################################   
    
class UserOrderListAPIView(generics.ListAPIView):
    
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
   
        qs=super().get_queryset()
            
        
        return qs.filter(user=self.request.user)
    
############################################################################################################ 
"""
 @api_view(['GET'])
def product_info(request):
    products= Product.objects.all()
    serializer = ProductInfoSerializer({
        'products' : products ,
        'count' : len(products) ,
        'max_price' : products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
 
 """   
class ProductInfoView(APIView):
    def get(self,request):
       
        products= Product.objects.all()
        serializer = ProductInfoSerializer({
            'products' : products ,
            'count' : len(products) ,
        'max_price' : products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)

#############################################################################################################