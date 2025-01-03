from django.db import models

class Ingredient_Type( models.Model ):
    name = models.CharField( max_length=30 )
    unit = models.CharField( max_length=10 )

    def __str__( self ):
        return self.name


class Ingredient( models.Model ):
    name = models.CharField( max_length=200 )
    desc = models.CharField( max_length=500 )
    ingredient_type = models.ForeignKey( Ingredient_Type, on_delete=models.CASCADE )

    def __str__( self ):
        return self.name


class Recipe( models.Model ):
    name = models.CharField( max_length=200 )
    url = models.URLField( max_length=200 )
    yield_volume = models.PositiveSmallIntegerField()
    yield_unit = models.CharField( max_length=10 )

    def __str__( self ):
        return self.name


class Recipe_Ingredient( models.Model ):
    recipe = models.ForeignKey( Recipe, on_delete=models.CASCADE )
    ingredient = models.ForeignKey( Ingredient, on_delete=models.PROTECT )
    qty = models.PositiveSmallIntegerField( 'quantity' )

    def __str__( self ):
        return f'<Recipe:{self.recipe.name} Ingredient:{self.ingredient.name} Qty:{self.qty}>'


class Vendor( models.Model ):
    name = models.CharField( max_length=200 )
    url = models.URLField( max_length=200 )

    def __str__( self ):
        return self.name


class Vendor_Ingredient( models.Model ):
    vendor = models.ForeignKey( Vendor, on_delete=models.CASCADE )
    ingredient = models.ForeignKey( Ingredient, on_delete=models.CASCADE )
    url = models.URLField( max_length=200 )
    price = models.DecimalField( max_digits=5, decimal_places=2 )
    unit_size = models.PositiveSmallIntegerField()

    def __str__( self ):
        return f'<Vendor:{self.recipe.name} Ingredient:{self.ingredient.name} Price:{self.price}>'
