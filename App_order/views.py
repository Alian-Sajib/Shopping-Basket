from django.shortcuts import render, get_object_or_404, redirect

# Authentication
from django.contrib.auth.decorators import login_required

# Models
from App_order.models import Order, Cart
from App_shop.models import Product

# Messages
from django.contrib import messages

# Create your views here.


@login_required
def add_to_cart(request, pk):
    # item which i want to add to cart
    item = get_object_or_404(Product, pk=pk)
    # print("Item: %s" % item)

    # check the item in the cart if yes then get or create it
    order_item = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False
    )
    # print("order_item:")
    # print(order_item)
    # print(order_item[0])
    # print(order_item[1])

    # check any order exits in the order list. false means not payment yet
    # the system provide one customer have only one running order.

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # print("order_qs: %s" % order_qs)

    if order_qs.exists():
        # accessing the object view first element. cause it save as tuple and we cant access it directly
        order = order_qs[0]

        # print("If oder exits")
        # print(order)

        # check if i added the item before in the cart
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item was updated")
            return redirect("App_shop:home")
        else:
            # many to many field add item
            order.orderitems.add(order_item[0])
            messages.info(request, "This item addded to your cart")
            return redirect("App_shop:home")

    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item addded to your cart")
        return redirect("App_shop:home")


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        return render(
            request, "App_order/cart.html", context={"carts": carts, "order": order}
        )
    else:
        messages.warning(request, "You are not add any item to cart")
        return redirect("App_shop:home")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False
            )[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was deleted from cart")
            return redirect("App_order:cart")
        else:
            messages.info(request, "This item was not found in cart")
            return redirect("App_shop:home")

    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_shop:home")


@login_required
def increase_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False
            )[0]

            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} item quantity increased")
                return redirect("App_order:cart")
            else:
                messages.warning(request, f"{item.name} is not in your cart")
                return redirect("App_order:home")

    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_shop:home")


@login_required
def decrease_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} item quantity decreased")
                return redirect("App_order:cart")
            else:
                # order.orderitems.remove(order_item)
                # order_item.delete()
                # messages.warning(request, f"{item.name} is removed from cart")
                return redirect("App_order:cart")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_shop:home")
