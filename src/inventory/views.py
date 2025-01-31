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


def edit( request ):
    # Inventory Editor
    data = {}
    for typ in Ingredient_Type.objects.all():
        # data[typ] = Ingredient.objects.filter( ingredient_type = typ )
        data.setdefault( typ, {} )
        for i in Ingredient.objects.filter( ingredient_type = typ ):
            data[typ][i] = 0 # initial change amount is zero
    if request.method == 'POST':
        # If data was POST'ed, then set the initial adjustment value to match
        for k,v in request.POST.items():
            if k.startswith( 'adj_'):
                adj = decimal.Decimal(v)
                ingr_name = k[4:]
                ingr = Ingredient.objects.get( name=ingr_name )
                data[ingr.ingredient_type][ingr] = adj
    context = { 'ingredient_types': data }
    return render( request, 'inventory/inventory_edit.html', context )


def update( request ):
    # Update Inventory based on POST'd data
    if request.method == 'POST':
        for k,v in request.POST.items():
            if k.startswith( 'adj_'):
                adj = decimal.Decimal(v)
                if adj != 0:
                    ingr_name = k[4:]
                    ingr = Ingredient.objects.get( name=ingr_name )
                    ingr.quantity_in_stock = ingr.quantity_in_stock + adj
                    ingr.save()
    # always redirect to Inventory
    rv = HttpResponseRedirect( reverse( "inventory:index" ) )
    return rv


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


def shopping_list( request ):
    if request.method == 'POST':
        # create shopping list for specified recipes
        recipes = []
        ingredients = {}
        for key, val in request.POST.items():
            if key.startswith( 'recipe_include_' ):
                recipe = Recipe.objects.get( name = val )
                recipes.append( recipe )
                recipe_ingredients = Recipe_Ingredient.objects.filter( recipe = recipe )
                for ri in recipe_ingredients:
                    i = ri.ingredient
                    last = ingredients.setdefault( i, {'needed':0, 'to_purchase':0} )
                    last['needed'] += ri.quantity_in_recipe
        for i, last in ingredients.items():
            if i.quantity_in_stock < last['needed']:
                last['to_purchase'] = last['needed'] - i.quantity_in_stock
        context = {
            'ingredients': ingredients,
            'recipes': recipes,
        }
        rv = render( request, 'inventory/shopping_list.html', context )
    else:
        # otherwise, redirect to list of recipes
        rv = HttpResponseRedirect(
            reverse( "inventory:recipe_list" )
            )
    return rv

def planner( request ):
    filters = []
    if request.method == 'POST':
        recipe_names = []
        ingredient_names = []
        for key, val in request.POST.items():
            if key.startswith( 'ingredient_include_' ):
                filters.append( val )
                # get recipes that use this ingredient
                i = Ingredient.objects.get( name = val )
                recipe_names.extend( [ x.recipe.name for x in i.recipe_ingredient_set.all() ] )
            if key.startswith( 'recipe_include_' ):
                filters.append( val )
                recipe_names.append( val )
        recipe_names = sorted( set( recipe_names ) )
        recipes = Recipe.objects.filter( name__in=recipe_names )
        for r in recipes:
            ingredient_names.extend( [ i.name for i in r.ingredients.all() ] )
        ingredient_names = sorted( set( ingredient_names ) )
        ingredients = Ingredient.objects.filter( name__in=ingredient_names )
    else:
        ingredients = Ingredient.objects.all()
        recipes = Recipe.objects.all()
    context = { 'filters': filters, 'ingredients': ingredients, 'recipes': recipes }
    return render( request, 'inventory/planner.html', context )
