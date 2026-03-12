from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from cart.forms import CartAddProductForm


#Remember for Tasks to run concurrently, one task has to give up event control(Using await)
#This is called cooperative multitasking, for CPU dependent event loop, Async is a bad idea
#This is because the task takes too long an execution time to give up control slowing concurrency or never gives it up at all
#So for CPU heavy tasks like image generation unlike network reques, db query or api calls, Use workers

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        print('slugggg')
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {'category': category,
        'categories': categories,
        'products': products
        }
        )

def product_detail(request, id, slug):
    product = get_object_or_404(
    Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
    request,
    'shop/product/detail.html',
    {'product': product,
     'cart_product_form':cart_product_form
     }
    )