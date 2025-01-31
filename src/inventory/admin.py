from django.contrib import admin
from .models import Ingredient, Ingredient_Type, Recipe

admin.site.register( Ingredient_Type )
admin.site.register( Ingredient )
admin.site.register( Recipe )
