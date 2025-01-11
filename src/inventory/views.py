from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Ingredient, Ingredient_Type, Recipe, Recipe_Ingredient
import pprint
import decimal


def index(request):
    # Inventory Report
    # Construct a dict of types with a list of ingredients of each type
    data = {}
    for typ in Ingredient_Type.objects.all():
        data[typ] = Ingredient.objects.filter( ingredient_type = typ )
    context = { 'ingredient_types': data }
    return render( request, 'inventory/inventory_list.html' , context )


class Recipe_List( generic.ListView ):
    model = Recipe


def recipe_detail( request, recipe_name ):
    # Gather recipe ingredients
    recipe = Recipe.objects.get( name=recipe_name )
    data = {}
    for ingr in recipe.ingredients.all():
        typ = ingr.ingredient_type
        r_ingr = Recipe_Ingredient.objects.get(
            Q( ingredient = ingr ) &
            Q( recipe = recipe )
            )
        data.setdefault( typ, [] ).append( { 'ingredient':ingr, 'recipe_ingredient':r_ingr } )
    context = { 'recipe': recipe, 'ingredient_types': data }
    return render( request, 'inventory/recipe_detail.html' , context )


def recipe_edit( request, recipe_name ):
    # Select ingredients and qty of each for a given recipe
    recipe = Recipe.objects.get( name=recipe_name )
    current_ingredients = recipe.ingredients.all()
    data = {}
    for typ in Ingredient_Type.objects.all():
        all_ingredients = Ingredient.objects.filter( ingredient_type = typ )
        data[typ] = { i.name: 0 for i in all_ingredients }
        for ingr in data[typ].keys():
            try:
                r_ingr = Recipe_Ingredient.objects.get( Q(ingredient__name = ingr) & Q(recipe = recipe) )
            except ObjectDoesNotExist:
                pass
            else:
                data[typ][ingr] = r_ingr.quantity_in_recipe
    context = { 'recipe': recipe, 'ingredient_types': data }
    return render( request, 'inventory/recipe_edit.html', context )


def recipe_update( request, recipe_name ):
    # Process request.POST'ed data to update the specified recipe
    recipe = Recipe.objects.get( name=recipe_name )
    # get all POSTed ingredients
    old = {}
    new = {}
    for k,v in request.POST.items():
        ingr_name = k[7:]
        if k.startswith( 'newval_' ):
            new[ingr_name] = decimal.Decimal(v)
        elif k.startswith( 'oldval_'):
            old[ingr_name] = decimal.Decimal(v)
    # find changed quantities and update just those
    for k in new.keys():
        if new[k] != old[k]:
            ingredient = Ingredient.objects.get( name=k )
            ( recipe_ingr, is_new ) = Recipe_Ingredient.objects.get_or_create(
                recipe = recipe,
                ingredient = ingredient,
                quantity_in_recipe = old[k]
                )
            if new[k] > 0:
                recipe_ingr.quantity_in_recipe = new[k]
                recipe_ingr.save()
            else:
                recipe_ingr.delete()
    return HttpResponseRedirect( reverse( "inventory:recipe_detail", args=( recipe_name, ) ) )


def shop( request ):
    if request.method == 'POST':
        # if POST, create shopping list for specified recipes
        rv = {}
    else:
        # otherwise, display list of recipes to choose from
        rv = {}
