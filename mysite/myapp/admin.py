from django.contrib import admin
from .models import product,orderdetails
from django.db.models import F
# Register your models here.
admin.site.site_header = "E-commerce Admin"
admin.site.site_title = "E-commerce Admin Portal"
admin.site.index_title = "Welcome to E-commerce Admin Portal"

class productADMIN(admin.ModelAdmin):
    list_display=('name','price','des')
    search_fields=('name','des',)
    def apply_discount(self,request,queryset):
        queryset.update(price=F('price')*0.9)
    
    actions =('apply_discount',)    
    list_editable=('price','des',)
    list_filter=('price',)


admin.site.register(product,productADMIN)
admin.site.register(orderdetails)
