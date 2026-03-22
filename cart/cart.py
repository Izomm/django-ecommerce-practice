from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

#Remember python has to serialize Session to JSOn (converting objects to string) because it has to save them in db or cache tha only accepts texts
#It is either Pickle format (fast but dangerous ) or JSON (Slow but safe)

'''
# These serialize fine 
str, int, float, bool, list, dict, None

# These DONT serialize || Needs conversion when they are to be serialized
Decimal, datetime, model instances, querysets
'''
class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
      
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
      
        
        self.cart = cart
          # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
             
                """
                Add a product to the cart or update its quantity.
                """

                #Product id converted into string cos django uses JSON to serialize session data
                #And json only allow string key names
                product_id = str(product.id)
                if product_id not in self.cart:
                    self.cart[product_id] = {
                    'quantity': 0,
                    'price': str(product.price)
                    }
                if override_quantity:
                    self.cart[product_id]['quantity'] = quantity
                else:
                    self.cart[product_id]['quantity'] += quantity

                self.save()

    def save(self):
                    # mark the session as "modified" to make sure it gets saved
                    self.session.modified = True

    def remove(self, product):
            """
            Remove a product from the cart.
            """
            product_id = str(product.id)
            if product_id in self.cart:
                #Alternative to pop, removes a dictionary reference
                del self.cart[
                    product_id]
                self.save()

    def __iter__(self):
            """
            Iterate over the items in the cart and get the products
            from the database.

            """

        
            product_ids = self.cart.keys()
            # get the product objects and add them to the cart
            products = Product.objects.filter(id__in=product_ids)

            #copy the cart  cos self.cart is stored in a session and we want to avoid mutating
            
            cart = self.cart.copy()
            
            
            for product in products:
                cart[str(product.id)]['product'] = product
            for item in cart.values():
                    item['price'] = Decimal(item['price'])
                    item['total_price'] = item['price'] * item['quantity']
                    #Doesnt build the list all into memory at once
                    #Retuns one value and continues from where it stops -Memory efficient
                    yield item

                    #So anytime you loop over a cart object, it gives you only one of this item at a time (one loop - one yileded item)
           
    def __len__(self):
            """
            Count all items in the cart."""
            return sum(item['quantity'] for item in self.cart.values())
        
    def get_total_price(self):
            return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
            )
        
    def clear(self):
            # remove cart from session
            del self.session[settings.CART_SESSION_ID]
            self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return (
            self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()