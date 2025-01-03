from django.contrib import admin

from .models import Ingredient, Ingredient_Type

admin.site.register( Ingredient_Type )
admin.site.register( Ingredient )
# admin.site.register( Recipe )
# admin.site.register( Recipe_Ingredient )
# admin.site.register( Vendor )
# admin.site.register( Vendor_Ingredient )
