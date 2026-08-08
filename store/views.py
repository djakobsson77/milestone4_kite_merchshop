from urllib import request

import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


def store(request):
    products = Product.objects.all().order_by('id')
    return render(request, "store/store.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def cart(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "The product you tried to add does not exist.")
        return redirect("store")

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
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
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
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
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
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
    item = CartItem.objects.get(id=item_id)
    item.product.stock += item.quantity
    item.product.save()
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')


def checkout(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
    cart_items = CartItem.objects.filter(user=request.user)

    # Beräkna subtotal för varje item
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    # Beräkna totalen
    total = sum(item.subtotal for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'store/checkout.html', context)


def create_checkout_session(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
    stripe.api_key = settings.STRIPE_SECRET_KEY

    cart_items = CartItem.objects.filter(user=request.user)

    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": item.product.name,
                },
                "unit_amount": int(item.product.price * 100),
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("checkout_success")),
        cancel_url=request.build_absolute_uri(reverse("checkout")),
    )

    return redirect(session.url)


def checkout_success(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            (
                "Only logged‑in users can order products. "
                "Please log in or sign up to continue."
            )
        )
        return redirect("login")
    # Clear cart after payment
    CartItem.objects.filter(user=request.user).delete()

    return render(request, "store/checkout_success.html")
