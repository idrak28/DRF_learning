import django_filters
from api.models import Product


class InstockFilterBaackend():
    def filter_queryset(self,request,queryset,view) :
        return queryset.filter(stock__gt=0) # remove 0 stock item
        #return queryset.exclude(stock__gt=0)    # only product have 0 stock


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields ={
            'name':['exact' , 'contains'],
            'price': ['exact', 'lt' ,'gt', 'range'] 
         }