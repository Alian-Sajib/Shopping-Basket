from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

# models and forms
from App_order.models import Order, Cart
from App_payment.models import BillingAddress
from App_payment.forms import BillingAddressForm

#
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# for payment
import requests
from sslcommerz_lib import SSLCOMMERZ

# from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket


# Create your views here.
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = BillingAddressForm(instance=saved_address)
    if request.method == "POST":
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, f"Shipping Address Saved !")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()

    return render(
        request,
        "App_payment/checkout.html",
        context={
            "form": form,
            "order_items": order_items,
            "order_total": order_total,
            "saved_address": saved_address,
        },
    )


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, "Please fill in your shipping address")
        return redirect("App_payment:checkout")

    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please fill in your profile information")
        return redirect("App_login:profile")

    store_id = "shopp66c9e603ca543"
    API_Key = "shopp66c9e603ca543@ssl"

    status_url = request.build_absolute_uri(
        reverse("App_payment:complete")
    )  # absolute uri return current url

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    current_user = request.user

    settings = {"store_id": store_id, "store_pass": API_Key, "issandbox": True}
    sslcommez = SSLCOMMERZ(settings)

    post_body = {}
    post_body["total_amount"] = order_total
    post_body["currency"] = "BDT"
    post_body["tran_id"] = "1234"
    post_body["success_url"] = status_url
    post_body["fail_url"] = status_url
    post_body["cancel_url"] = status_url
    post_body["emi_option"] = 0
    post_body["cus_name"] = current_user.profile.full_name
    post_body["cus_email"] = current_user.email
    post_body["cus_phone"] = current_user.profile.phone
    post_body["cus_add1"] = current_user.profile.address_1
    post_body["cus_city"] = current_user.profile.city
    post_body["cus_country"] = current_user.profile.country
    post_body["shipping_method"] = "Courier"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = order_items_count
    post_body["product_name"] = order_items
    post_body["product_category"] = "Mixed"
    post_body["product_profile"] = "general"
    post_body["ship_name"] = current_user.profile.full_name
    post_body["ship_add1"] = current_user.profile.address_1
    post_body["ship_postcode"] = current_user.profile.zipcode
    post_body["ship_city"] = current_user.profile.city
    post_body["ship_country"] = current_user.profile.country

    response = sslcommez.createSession(post_body)
    # print(response)
    return redirect(response["GatewayPageURL"])


@csrf_exempt
def complete(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST
        status = payment_data["status"]

        if status == "VALID":
            val_id = payment_data["val_id"]
            bank_tran_id = payment_data["bank_tran_id"]
            messages.success(request, "Payment Successful!")
            return HttpResponseRedirect(
                reverse(
                    "App_payment:purchase",
                    kwargs={"val_id": val_id, "bank_tran_id": bank_tran_id},
                )
            )
        elif status == "FAILED":
            messages.warning(request, "Payment Failed!")
    return render(request, "App_payment/complete.html", context={})


@login_required
def purchase(request, val_id, bank_tran_id):
    # update order information
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.orderId = val_id
    order.paymentId = bank_tran_id
    order.save()
    # update Cart information
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("App_shop:home"))


@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user)
        context = {"orders": orders}
    except:
        messages.warning(request, "You haven't an active order")
        return redirect("App_shop:home")
    
    return render(request, "App_payment/orders.html", context={"orders": orders})
