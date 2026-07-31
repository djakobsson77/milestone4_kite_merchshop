from django.shortcuts import render, get_object_or_404
from .models import Product, CartItem
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def store(request):
    products = Product.objects.all()
    return render(request, "store/store.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})

def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # If product is out of stock
    if product.stock <= 0:
        messages.error(request, "This item is out of stock.")
        return redirect(f"/store/#{product.category}")

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    # If product already is in cart
    if not created:
        # check that we do not exceed stock balance
        if product.stock <= 0:
            messages.error(request, "Not enough stock available.")
            return redirect(f"/store/#{product.category}")

        cart_item.quantity += 1
        cart_item.save()

         # decrease stock
        product.stock -= 1
        product.save()

    else:
        # new cart item → decrease stock
        product.stock -= 1
        product.save()

    messages.info(request, "Added to cart.")
    return redirect(f"/store/#{product.category}")

def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)

    if item.product.stock > 0:
        item.quantity += 1
        item.save()
        item.product.stock -= 1
        item.product.save()
    else:
        messages.error(request, "Not enough stock available.")

    return redirect('cart')


def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)

    item.product.stock += 1
    item.product.save()

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.product.stock += item.quantity
    item.product.save()
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')
