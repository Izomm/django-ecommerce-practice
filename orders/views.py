from cart.cart import Cart
from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                print(item)
                

                OrderItem.objects.create(
                        order=order,
                        product= item['product'] , # use .get() To return None incase it doesnt exist
                        price=item['price'],
                        quantity=item['quantity']
                        )
                
                

                # clear the cart
            cart.clear()
                # launch asynchronous task
            order_created.delay(order.id)
            return render(
                request, 'orders/order/created.html', {'order': order}
                )
    else:
        form = OrderCreateForm()
    return render(
                request,
                'orders/order/create.html',
                {'cart': cart, 'form': form}
                )