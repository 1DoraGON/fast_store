
from email.policy import default
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from chargily_epay_django.models import AnonymPayment,FakePaymentMixin
from django.utils.text import slugify 
from django.utils.crypto import get_random_string


from autoslug import AutoSlugField

from core.constants import LABEL_CHOICES, DELIVERY_MODE, PAYMENT_CANCELED, PAYMENT_EXPIRED, PAYMENT_FAILED, PAYMENT_IN_PROGRESS, PAYMENT_PAID, WILAYA
from core.forms import PAYMENT_MODE


# Create your models here.


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    zip = models.CharField(max_length=20)
    wilaya = models.CharField(choices = WILAYA, max_length=100)    
    apartment = models.CharField(max_length=200)    
    address1 = models.CharField(max_length=200)    
    address2 = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return f"{self.id}- {self.user.username} address: {self.address1}"    

class Category(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    def get_items_count(self):
        count = Item.objects.filter(category=self).count()
        return count
    def get_sold_items(self):
        items = Item.objects.filter(category=self)
        sold = 0
        for item in items:
            sold += item.sold
        return sold
    def __str__(self):
        return self.name
class Item(models.Model):
    title = models.CharField(max_length=100)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1 , default='P')
    price = models.FloatField()
    discount_price = models.FloatField(blank=True , null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title',unique=True)
    description = models.TextField()
    quantity = models.IntegerField(default = -1)
    sold = models.IntegerField(default = 0)
    total_amount = models.IntegerField(default = 0)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("core:item-detail", kwargs={"slug": self.slug})
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        random_string = get_random_string(8,'0123456789')
        self.slug = slugify(f"{self.pk,self.title}")
        super(Item, self).save(*args, **kwargs)
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})
    
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item , on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    ordered = models.BooleanField(default=False)
    order_confirmed = models.BooleanField(default=False)
    quantity = models.IntegerField(default = 1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        return self.item.price * self.quantity
    def get_total_item_price_discount(self):
        return self.item.discount_price * self.quantity
        
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_price_discount()
        
    def get_item_total(self):
        if(self.item.discount_price):
            return self.get_total_item_price_discount()
        else:
            return self.get_total_item_price()
class Coupon(models.Model):
    code = models.CharField(max_length=15,unique=True)
    used = models.BooleanField(default=False)
    discount = models.IntegerField()
    def __str__(self):
        return f"{self.code} used: {'used' if self.used else 'not yet'}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    coupon = models.ForeignKey(Coupon,blank=True,null=True,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_item_total()
        return total

PAYMENT_STATUS = {
    (PAYMENT_EXPIRED, "EXPIRED"),
    (PAYMENT_IN_PROGRESS, "IN PROGRESS"),
    (PAYMENT_PAID, "PAID"),
    (PAYMENT_FAILED, "FAILED"),
    (PAYMENT_CANCELED, "CANCELED"),
}

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    payment_mode = models.CharField(choices=PAYMENT_MODE, max_length = 100)
    delivery_mode = models.CharField(choices=DELIVERY_MODE, max_length = 100)
    invoice = models.CharField(max_length=20,unique=True)
    status = models.CharField(
        max_length=25, default=PAYMENT_IN_PROGRESS, choices=PAYMENT_STATUS
    )
    def __str__(self):
        return f"{self.invoice} total: {self.order.get_total_price()}"

class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.first_name} {self.user.first_name}"

class File(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    file = models.FileField(upload_to=f'images/%Y/%m/%d')