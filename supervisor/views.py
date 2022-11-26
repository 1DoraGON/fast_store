from django.shortcuts import render
from pprint import pprint
from django.views.generic import FormView,ListView, TemplateView
from django.conf import settings
from supervisor.forms import CategoryForm, SupervisorForm, ItemForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from allauth.account.utils import get_user_model
from core.models import Category, Item, Supervisor,File
from django.shortcuts import redirect,reverse
from django.http import JsonResponse, HttpResponseNotAllowed
from core.utils import has_related_supervisor
from supervisor.mixins import SupervisorMixin

from django.core.files.storage import FileSystemStorage

from ecommerce import settings
# Create your views here.
User = get_user_model()

def dashboard(request):
    return render(request,'supervisor/charts.html')

class ItemList(SupervisorMixin,ListView):
    template_name= "supervisor/tables.html"
    model = Item
    context_object_name = "items"

class CreateItemView(FormView):
    def get(self,*args, **kwargs):
        context = {
            'form' : ItemForm()
        }
        return render(self.request,'supervisor/management/add-item.html',context)
    def post(self, *args, **kwargs):
        form = ItemForm(self.request.POST,self.request.FILES)
        files = self.request.FILES.getlist('image')
        if form.is_valid():
            title = form.cleaned_data['title']
            label = form.cleaned_data['label']
            price = form.cleaned_data['price']
            discount_price = form.cleaned_data['discount_price']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            quantity = form.cleaned_data['quantity']
            for f in files:
                ext = f.name.split(".")[-1].lower()
                if not ext in settings.ACCEPTED_FILES:
                    messages.warning(self.request
                    ,f'This file format is not supported! Please upload {settings.ACCEPTED_FILES} formats')
                    return redirect('supervisor:add-item')
            item = Item(
                title=title,
                label=label,
                price=price,
                discount_price=discount_price,
                category=category,
                description=description,
                quantity=quantity
            )
            item.save()
            if item:
                for f in files:
                    image = File(item= item,file = f)
                    image.save()
                messages.success(self.request,'Item added!')
                return redirect('supervisor:add-item')
            else:
                messages.info(self.request,'Error occured, try again !')
                return redirect('supervisor:add-item')
        else:
            messages.info(self.request,'Form is not valid, try again !')
            return redirect('supervisor:add-item')            
class CategoryListView(SupervisorMixin,ListView):
    def get(self, *args, **kwargs):
        form = CategoryForm()
        categories = Category.objects.all()
        context = {
            "categories" : categories,
            "category_form" : form
        }
        return render(self.request,'supervisor/categories.html',context=context)
    def post(self,*args, **kwargs):
        form = CategoryForm(self.request.POST) or None
        if form.is_valid():
            category = Category(name = form.cleaned_data["category_name"])
            category.save()
            return redirect('supervisor:categories')

        return redirect(self.request,'supervisor:categories')
class CreateSupervisorView(SupervisorMixin,FormView):
    template_name= "add-supervisor.html"
    form_class = SupervisorForm
    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data['email'])
            is_admin = form.cleaned_data['supervisor_type']
            supervisor = Supervisor(
                user = user,
                is_admin = is_admin
            )
#            supervisor.save()
            pprint(supervisor)
            messages.success(self.request,'Supervisor added!')
            return redirect('supervisor:dashboard')

        except ObjectDoesNotExist:
            messages.warning(self.request,'Email does not exist')
            return redirect('supervisor:add-supervisor')
        
def add_category(request):
    try:
        name = request.POST
        pprint(request)
        messages.success(request,'Cateory added!')
        return reverse('core:item-list')
        new_category = Category(
            name = name
        )
        new_category.save()
    except ObjectDoesNotExist:
        messages.warning(request,'The form is invalid!')
        return reverse('core:item-list')


def get_email(request):
    supervisor_required(request.user)
    email = request.GET['email']
    responseUsers = User.objects.filter(email__startswith=email)[:5]
    responseEmails = []
    for responseUser in responseUsers:
        responseEmails.append(responseUser.email)
    pprint(responseEmails)
    return JsonResponse({
        'emails':responseEmails
    })

def supervisor_required(user):
    if has_related_supervisor(user):
        if user.supervisor.is_admin:
            return True
        return HttpResponseNotAllowed("Not allowed")
    else:
        return HttpResponseNotAllowed("Not allowed")