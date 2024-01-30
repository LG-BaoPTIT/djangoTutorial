from django.shortcuts import render
from django.template import RequestContext 
from cart import cart 

# Create your views here.
def show_cart(request, template_name="cart/cart.html"):
    cart_item_count = cart.cart_item_count(request)
    page_title = 'Shopping Cart'
    return render(request, template_name, locals())

