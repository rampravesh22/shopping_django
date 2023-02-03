from .forms import CustomerProfileForm
from django.contrib import messages
from .forms import CustomerRegisterationForm
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import *
from django.http import JsonResponse


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category="TW")
        bottomwears = Product.objects.filter(category="BW")
        mobiles = Product.objects.filter(category="M")

        context = {
            "topwears": topwears,
            "bottomwears": bottomwears,
            "mobiles": mobiles,
        }
        return render(request, 'app/home.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return render(request, 'app/productdetail.html', {"product": product})


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, 'app/profile.html', {'form': form, 'active': "btn-primary"})

    def post(self, request):
        form = CustomerProfileForm(data=request.POST)
        if form.is_valid():
            usr = request.user
            data = form.cleaned_data
            name = data['name']
            state = data['state']
            city = data['city']
            locality = data['locality']
            zipcode = data['zipcode']

            Customer.objects.create(
                user=usr, name=name, locality=locality, state=state, city=city, zipcode=zipcode
            )

            messages.success(request, "Congratulation !! Profile updated")
        return render(
            request, 'app/profile.html', {'form': form, 'active': "btn-primary"})


def product_detail(request):
    return render(request, 'app/productdetail.html')


def add_to_cart(request):
    user = request.user
    prod_id = request.GET.get("prod_id")
    product = Product.objects.get(id=prod_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = p.quantity*p.product.discounted_price
                amount += temp_amount
                total_amount = amount + shipping_amount
            return render(
                request, 'app/addtocart.html', {'carts': cart, "total_amount": total_amount, "amount": amount})

        else:
            return render(request, "app/emptycart.html")


def plus_cart(request):
    if request.method == "GET":
        prod_id = int(request.GET.get('prod_id'))
        print(prod_id)

        print("**********************************************")
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [
            p for p in Cart.objects.all() if p.user == request.user
        ]
        for p in cart_product:
            temp_amount = p.quantity*p.product.discounted_price
            amount += temp_amount
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            "amount": amount,
            "total_amount": total_amount
        }

        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


# def profile(request):
#     return render(request, 'app/profile.html')


def address(request):
    add = Customer.objects.filter(user=request.user)

    return render(request, 'app/address.html', {"address": add, "active": "btn-primary"})


def orders(request):
    return render(request, 'app/orders.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category="M")

    elif data == "redmi" or data == "samsung":
        data = data.lower()
        mobiles = Product.objects.filter(
            category="M").filter(brand=data)

    elif data == "below10000":
        mobiles = Product.objects.filter(
            category="M").filter(discounted_price__lt=10000)

    elif data == "above10000":
        mobiles = Product.objects.filter(
            category="M").filter(discounted_price__gt=10000)
    context = {
        'mobiles': mobiles
    }
    return render(request, 'app/mobile.html', context)


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegisterationForm()
        return render(request, 'app/customerregistration.html', {"form": form})

    def post(self, request):
        form = CustomerRegisterationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")

        return render(request, 'app/customerregistration.html', {"form": form})


def checkout(request):
    return render(request, 'app/checkout.html')
