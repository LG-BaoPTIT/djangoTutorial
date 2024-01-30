from django.template import RequestContext
import cart
from .models import CartItem 
from catalog.models import Product 
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect 
import decimal 
import random 

CART_ID_SESSION_KEY = 'cart_id' 

# get the current user's cart id, sets new one if blank 
def _cart_id(request): 
    if request.session.get(CART_ID_SESSION_KEY,'') == '': 
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id() 
    return request.session[CART_ID_SESSION_KEY] 
def _generate_cart_id(): 
    cart_id = '' 
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()' 
    cart_id_length = 50 
    for y in range(cart_id_length): 
        cart_id += characters[random.randint(0, len(characters)-1)] 
    return cart_id 
# return all items from the current user's cart 
def get_cart_items(request): 
    return CartItem.objects.filter(cart_id=_cart_id(request)) 
# add an item to the cart 
def add_to_cart(request): 
    postdata = request.POST.copy() 
    # get product slug from post data, return blank if empty 
    product_slug = postdata.get('product_slug','') 
    # get quantity added, return 1 if empty 
    quantity = postdata.get('quantity',1) 
    # fetch the product or return a missing page error 
    p = get_object_or_404(Product, slug=product_slug) 
    #get products in cart 
    cart_products = get_cart_items(request) 
    product_in_cart = False 
    # check to see if item is already in cart 
    for cart_item in cart_products: 
        if cart_item.product.id == p.id: 
            cart_item.augment_quantity(quantity) 
            product_in_cart = True 
    if not product_in_cart: 
    # create and save a new cart item 
        ci = CartItem() 
        ci.product = p 
        ci.quantity = quantity 
        ci.cart_id = _cart_id(request) 
        ci.save() 
# returns the total number of items in the user's cart 
def cart_item_count(request): 
    return get_cart_items(request).count()

def show_cart(request, template_name="cart/cart.html"): 
    if request.method == 'POST': 
        postdata = request.POST.copy() 
        if postdata['submit'] == 'Remove': 
            cart.remove_from_cart(request) 
        if postdata['submit'] == 'Update': 
            cart.update_cart(request) 
    cart_items = cart.get_cart_items(request) 
    page_title = 'Shopping Cart' 
    cart_subtotal = cart.cart_subtotal(request) 
    return render(request, template_name, locals())

def get_single_item(request, item_id): 
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request)) 

def update_cart(request): 
    postdata = request.POST.copy() 
    item_id = postdata['item_id'] 
    quantity = postdata['quantity'] 
    cart_item = get_single_item(request, item_id) 
    if cart_item:
        if int(quantity) > 0: 
            cart_item.quantity = int(quantity) 
            cart_item.save() 
        else: 
            remove_from_cart(request) 
            
def remove_from_cart(request): 
    postdata = request.POST.copy() 
    item_id = postdata['item_id'] 
    cart_item = get_single_item(request, item_id) 
    if cart_item: 
        cart_item.delete() 
        
# gets the total cost for the current cart 
def cart_subtotal(request): 
    cart_total = decimal.Decimal('0.00') 
    cart_products = get_cart_items(request) 
    for cart_item in cart_products: 
        cart_total += cart_item.product.price * cart_item.quantity 
    return cart_total

def is_empty(request): 
    return cart_item_count(request) == 0 

def empty_cart(request): 
    user_cart = get_cart_items(request) 
    user_cart.delete() 