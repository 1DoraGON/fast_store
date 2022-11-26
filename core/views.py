from multiprocessing import context
from pprint import pprint
from random import randint, random, randrange
import requests
from core.constants import PAYMENT_FAILED
from core.forms import CheckoutForm
from core.utils import has_related_object, has_related_supervisor




from ecommerce import settings, urls



from django.utils import timezone
from django.shortcuts import render, get_object_or_404 , redirect , reverse

from supervisor.forms import CategoryForm
from .models import Address, Category, Coupon, Item, Order, OrderItem, Payment
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class ItemList(ListView):
    template_name= "home-page.html"
    context_object_name= "items"
    def get_queryset(self):
        return Item.objects.all()
    paginate_by= 1
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            user = self.request.user
            is_supervisor = has_related_supervisor(user)
        else:
            is_supervisor = False
        context = super().get_context_data(**kwargs)
        context['path'] = "/"
        context['categories'] = Category.objects.all()
        context['is_supervisor'] = is_supervisor
        return context

class OrderSummaryView(LoginRequiredMixin,DetailView):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            context = {
                'order': order
            }
            return render(self.request, 'order-summary.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name= "product-page.html"
    context_object_name= "item"

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item , slug = slug)
    order_item,created = OrderItem.objects.get_or_create(item = item,
    user = request.user,
    ordered = False, description ='something')
    order_qs = Order.objects.filter(user = request.user , ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request , "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request , "This item was added to your cart")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user = request.user ,
            ordered_date = ordered_date,
        )
        order.items.add(order_item)
        messages.info(request , "This item was added to your cart")
        return redirect("core:order-summary")

@login_required
def remove_from_cart(request , slug):
    item = get_object_or_404(Item , slug = slug)
    order_qs = Order.objects.filter(user = request.user , ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item = item,
                user = request.user,
                ordered = False)[0]
            order.items.remove(order_item)
            messages.info(request , "This item was removed from your cart")
            return redirect("core:item-detail" ,slug = slug)
        else:
            messages.info(request , "This item does not exist in your cart")
            return redirect("core:item-detail" ,slug = slug)
    else:
        messages.info(request , "You dont have an ongoing order yet")
        return redirect("core:item-detail" ,slug = slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

class CheckoutView(LoginRequiredMixin,FormView):

    def get(self, *args,**kwargs):
        user = self.request.user
        form = CheckoutForm()
        if has_related_object(user):
            address = user.address
            if address:
                form.fields['address1'].widget.attrs["value"] = address.address1
                form.fields['address2'].widget.attrs["value"] = address.address2
                form.fields['zip'].widget.attrs["value"] = address.zip
                form.fields['wilaya'].widget.attrs["value"] = address.wilaya
                form.fields['apartment_address'].widget.attrs["value"] = address.apartment
        context = {
            'form' : form
        }
        return render(self.request, 'checkout-page.html',context)

    def post(self , *args,**kwargs):
        form = CheckoutForm(self.request.POST) or None
        user = self.request.user
        if form.is_valid():
            try:
                order = Order.objects.get(user=user, ordered = False)
                receiver_firstname = form.cleaned_data.get('receiver_firstname')
                receiver_lastname = form.cleaned_data.get('receiver_lastname')
                wilaya = form.cleaned_data.get('wilaya')
                address1 = form.cleaned_data.get('address1')
                address2 = form.cleaned_data.get('address2')
                apartment_address = form.cleaned_data.get('apartment_address')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                payment_option = form.cleaned_data.get('payment_option')
                delivery_mode = form.cleaned_data.get('delivery_mode')
                if has_related_object(user):
                    address=user.address
                    address.zip=zip,
                    address.wilaya=wilaya,
                    address.address1=address1,
                    address.address2=address2,
                    address.apartment=apartment_address,
                    address.save()
                else:
                    address =Address(
                        user=user,
                        zip=zip,
                        wilaya= wilaya,
                        address1 = address1,
                        address2 = address2,
                        apartment = apartment_address,
                    )
                    address.save()
                payment = Payment(
                    user = user,
                    order = order,
                    address = address,
                    first_name = receiver_firstname,
                    last_name = receiver_lastname,
                    phone = phone,
                    delivery_mode = delivery_mode,
                    payment_mode = payment_option,
                    invoice = f"{randrange(10000,99999)}{order.id}"
                )
                payment.save()
                url = 'https://epay.chargily.com.dz/api/invoice'
                headers = { "X-Authorization" : settings.CHARGILY_API_KEY,
                            "Accept" : "application/json"}
                back_url = "https://google.com"
                webhook_url = "https://jsonplaceholder.typicode.com/posts"
                amount =order.get_total_price()
                if order.coupon:

                    discount = (order.coupon.discount/amount)*100 if order.coupon.discount < amount else 99.99
                else:
                    discount = 0
                if (amount - (discount*amount)/100) < 75:
                    discount = (amount-75)/amount 
                myobj = {
                    "client": user.username,
                    "client_email": user.email,
                    "invoice_number": payment.invoice,
                    "amount": amount,
                    "discount": discount,
                    "back_url": back_url,
                    "webhook_url": webhook_url,
                    "mode" : payment.payment_mode,
                    "comment": "comment"
                }
                print(myobj)
                
                x = requests.post(url, data = myobj, headers=headers) or None
                pprint(x)
                if x.status_code==201:

                    d = eval(x.text)["checkout_url"].replace('\\','') or None
                    return redirect(d)
                else:
                    payment.status = PAYMENT_FAILED
                    payment.save()
                    messages.warning(self.request,'An error occured, please try again!')
                    return redirect('core:checkout')
                    



            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect("/")
        messages.warning('form is not valid')
        return redirect(self.request,'core:checkout')


def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code = code)
        if coupon.used:
            messages.warning(request,'This coupon is already used!')
            return redirect('core:checkout')
        return coupon
    except Coupon.DoesNotExist:
        messages.warning(request,'This coupon does not exist')
        return redirect('core:checkout')

def add_coupon(request):
    try:
        code = request.POST['code']
        order = Order.objects.get(user = request.user, ordered = False)
        order.coupon = get_coupon(request,code)
        order.save()
        order.coupon.used=True
        order.save()
        messages.success(request,'Coupon added successfully!')
        return redirect('core:checkout')
    except ObjectDoesNotExist:
        messages.info(request,'You do not have an active order!')
        return redirect('core:item-list')

""" class CheckoutUpdateView(LoginRequiredMixin,UpdateView) """