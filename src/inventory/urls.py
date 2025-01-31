from django.urls import path

from . import views

app_name = "inventory"
urlpatterns = [
    path( "", views.index, name="index" ),
    path( "edit/", views.edit, name="inventory_edit" ),
    path( "update/", views.update, name="inventory_update" ),
    path( "recipe/", views.Recipe_List.as_view(), name="recipe_list" ),
    path( "recipe/<recipe_name>/", views.recipe_detail, name="recipe_detail" ),
    path( "recipe/<recipe_name>/edit/", views.recipe_edit, name="recipe_edit" ),
    path( "recipe/<recipe_name>/update/", views.recipe_update, name="recipe_update" ),
    path( "shopping_list/", views.shopping_list, name="shopping_list" ),
    path( "planner/", views.planner, name="planner" ),
]
