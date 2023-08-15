from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect

# Create your views here.
def homePageView(request):
    return HttpResponse("testing")

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "Practice page ",
        "author": "Developed by: Andres Leonardo Rojas Peña",
        })

        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "phone_number": "3116003325",
        "email": "test@eafit.edu.co",
        "address": "barrio antioquia con quinta avenida"        
        })

        return context
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"It's a very big TV", "price":2500},
        {"id":"2", "name":"iPhone", "description":"¿Why not an iPhone?", "price":55000000000},
        {"id":"3", "name":"Chromecast", "description":"Just a Chromecast haha", "price":50},
        {"id":"4", "name":"Glasses", "description":"Cheap Glasses, it are cool","price":99 }
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id)-1]
        except:
            return HttpResponseRedirect("/")
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    description = forms.CharField(required=False)

    def clean_price(self):
        price = self.cleaned_data['price']
        if (price <= 0):
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    

class ProductCreateView(View):
    template_name = 'products/create.html'
    created_product = 'products/create_product.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    def post(self, request):
        form = ProductForm(request.POST)
        viewData = {}
        viewData["form"] = form.data
        if form.is_valid():
            #print(form.data['name'])
            id = len(Product.products)+1
            Product.products.append({"id":id, "name":form.data['name'], "description":form.data['description'], "price":int(form.data['price'])})
            return render(request,self.created_product,viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)