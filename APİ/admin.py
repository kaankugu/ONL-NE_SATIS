from . models import *
from django.contrib import admin
 
admin.site.register(CustomUser)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 15  

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)