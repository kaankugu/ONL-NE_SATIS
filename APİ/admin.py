from django.contrib import admin
from . models import *
 
admin.site.register(CustomUser)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 15  

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)