from django.shortcuts import render
from django.shortcuts import get_object_or_404
from catalog.models import Category, Product 
from django.template import RequestContext
from django.urls import resolve
from cart import cart
from django.http import HttpResponseRedirect 
from cart.forms import ProductAddToCartForm 
# Create your views here.
def index(request, template_name="catalog/index.html"): 
    page_title = 'Musical Instruments and Sheet Music for Musicians' 
    print(1)

    return render(template_name, locals(), context_instance=RequestContext(request)) 

def show_category(request, category_slug, template_name="catalog/category.html"): 
    c = get_object_or_404(Category, slug=category_slug) 
    products = c.product_set.all() 
    page_title = c.name 
    meta_keywords = c.meta_keywords 
    meta_description = c.meta_description
    print(2)

    context = {
        'c': c,
        'products': products,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
    }
    return render(request, template_name, context)



def show_product(request, product_slug, template_name="catalog/product.html"): 
    print(3)

    p = get_object_or_404(Product, slug=product_slug) 
    categories = p.categories.filter(is_active=True) 
    page_title = p.name 
    meta_keywords = p.meta_keywords 
    meta_description = p.meta_description 
    if request.method == 'POST': 

 # add to cart…create the bound form 
        postdata = request.POST.copy() 
        form = ProductAddToCartForm(request, postdata) 
 #check if posted data is valid 
        if form.is_valid():
            cart.add_to_cart(request) 
        if request.session.test_cookie_worked(): 
            request.session.delete_test_cookie() 
        url = resolve.reverse('show_cart') 
        return HttpResponseRedirect(url) 
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
        form.fields['product_slug'].widget.attrs['value'] = product_slug 
        request.session.set_test_cookie() 
        
    context = {
        'p': p,
        'categories': categories,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'form': form,
    }

    return render(request, template_name, context)