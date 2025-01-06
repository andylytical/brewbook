from django.contrib import admin
from .models import Ingredient, Ingredient_Type, Recipe, Recipe_Ingredient
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
# import_export see also
# https://django-import-export.readthedocs.io/en/latest/advanced_usage.html#declare-fields
# https://django-import-export.readthedocs.io/en/latest/advanced_usage.html#import-model-relations


class Ingredient_Type_Resource( resources.ModelResource ):
    class Meta:
        model = Ingredient_Type
        # import_id_fields = ( 'name' )
        # exclude = ( 'id' )

@admin.register( Ingredient_Type )
class Ingredient_Type_Admin( ImportExportModelAdmin ):
    resource_classes = [ Ingredient_Type_Resource ]


class Ingredient_Resource( resources.ModelResource ):
    ingredient_type = fields.Field(
        column_name = 'ingredient_type',
        attribute = 'ingredient_type',
        widget = ForeignKeyWidget( Ingredient_Type, field='name' ) )

    class Meta:
        model = Ingredient
        # import_id_fields = ( 'name' )
        # exclude = ( 'id' )

@admin.register( Ingredient )
class Ingredient_Admin( ImportExportModelAdmin ):
    resource_classes = [ Ingredient_Resource ]


class Recipe_Resource( resources.ModelResource ):
    class Meta:
        model = Recipe

@admin.register( Recipe )
class Recipe_Admin( ImportExportModelAdmin ):
    resource_classes = [ Recipe_Resource ]


class Recipe_Ingredient_Resource( resources.ModelResource ):
    recipe = fields.Field(
        column_name = 'recipe',
        attribute = 'recipe',
        widget = ForeignKeyWidget( Recipe, field='name' ) )

    ingredient = fields.Field(
        column_name = 'ingredient',
        attribute = 'ingredient',
        widget = ForeignKeyWidget( Ingredient, field='name' ) )

    class Meta:
        model = Recipe_Ingredient

@admin.register( Recipe_Ingredient )
class Recipe_Admin( ImportExportModelAdmin ):
    resource_classes = [ Recipe_Ingredient_Resource ]

# admin.site.register( Recipe )
# admin.site.register( Recipe_Ingredient )
# admin.site.register( Vendor )
# admin.site.register( Vendor_Ingredient )
