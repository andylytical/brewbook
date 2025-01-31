from django.db import models

class Ingredient_Type( models.Model ):
    name = models.CharField( max_length=30, unique=True )
    unit = models.CharField( max_length=10 )

    def __str__( self ):
        return self.name


class Ingredient( models.Model ):
    name = models.CharField( max_length=200, unique=True )
    desc = models.CharField( max_length=500, blank=True )
    ingredient_type = models.ForeignKey( Ingredient_Type, on_delete=models.CASCADE )
    quantity_in_stock = models.PositiveSmallIntegerField( default=0 )

    def __str__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]


class Recipe( models.Model ):
    name = models.CharField( max_length=200, unique=True )
    url = models.URLField( max_length=200, blank=True )
    yield_volume = models.PositiveSmallIntegerField()
    yield_unit = models.CharField( max_length=10 )
    notes = models.TextField( blank=True )
    ingredients = models.ManyToManyField( Ingredient, through="Recipe_Ingredient" )

    def __str__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]


class Recipe_Ingredient( models.Model ):
    recipe = models.ForeignKey( Recipe, on_delete=models.CASCADE )
    ingredient = models.ForeignKey( Ingredient, on_delete=models.PROTECT )
    quantity_in_recipe = models.DecimalField( max_digits=5, decimal_places=2 )
    # option_group = models.PositiveSmallIntegerField( 'Equivalent Alternatives', blank=True )

    def __str__( self ):
        return f'<{self.recipe.name} - {self.ingredient.name} ({self.quantity_in_recipe} {self.ingredient.ingredient_type.unit})>'

    class Meta:
        unique_together = [ [ 'recipe', 'ingredient' ] ]


# class Vendor( models.Model ):
#     name = models.CharField( max_length=200, unique=True )
#     url = models.URLField( max_length=200 )

#     def __str__( self ):
#         return self.name

#     class Meta:
#         ordering = [ 'name' ]


# class Vendor_Ingredient( models.Model ):
#     vendor = models.ForeignKey( Vendor, on_delete=models.CASCADE )
#     ingredient = models.ForeignKey( Ingredient, on_delete=models.CASCADE )
#     url = models.URLField( max_length=200, blank=True )
#     price = models.DecimalField( max_digits=5, decimal_places=2 )
#     unit_size = models.PositiveSmallIntegerField()

#     def __str__( self ):
#         return f'<Vendor:{self.recipe.name} Ingredient:{self.ingredient.name} Price:{self.price}>'

#     class Meta:
#         unique_together = [ [ 'vendor', 'ingredient' ] ]
