# See also:
# https://codemax.app/snippet/how-to-create-a-dynamic-menu-in-django/
def topnav_menu( request ):
    menu_items = []
    menu_items.append( { 'url': 'inventory:index', 'label': 'Inventory' } )
    menu_items.append( { 'url': 'inventory:recipe_list', 'label': 'Recipes' } )
    menu_items.append( { 'url': 'inventory:planner', 'label': 'Planner' } )
    return { 'topnav_menu': menu_items }
