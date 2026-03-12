from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        #does it duplicate or replace
        cart.add(
        product=product,
        quantity=cd['quantity'],
        override_quantity=cd['override']
        )
        # print(f'-----skr {cart.cart}')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    #This line gets the saved cart from session 
    cart = Cart(request)

    print(type(cart))
    print(type(cart.cart))
    cart_items = list(cart)  
    

    
    for item in cart_items:
            print(f'-----skr {item}')
            item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
            )


    return render(request, 'cart/detail.html', {'cart': cart_items})