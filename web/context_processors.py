from decimal import Decimal
from django.shortcuts import get_object_or_404
from .cart import Cart
from .models import Product, Wishlist  # Import your Wishlist model

def main_context(request):
    cart = Cart(request)
    cart_items = []
    cart_count = 0

    for item_id, item_data in cart.get_cart():
        product = get_object_or_404(Product, id=item_id)
        quantity = item_data['quantity']
        total_price = Decimal(item_data['price']) * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

        cart_count += quantity

    # Fetch wishlist items for the logged-in user
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        for item in wishlist:
            product = get_object_or_404(Product, id=item.product.id)
            wishlist_items.append(product)

    context = {
        'cart_items': cart_items,
        'cart_total': cart.cart_total(),
        'cart_count': cart_count,
        'wishlist_items': wishlist_items,  # Add wishlist items to the context
        'wishlist_count': len(wishlist_items),  # Wishlist count
    }

    return context