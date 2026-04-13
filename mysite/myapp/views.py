from django.shortcuts import render
from django.http import HttpResponse
from .models import product,orderdetails
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import HttpResponseNotFound,JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import TemplateView
import stripe
from django.urls import reverse
# Create your views here.
def index(requests):
    return HttpResponse("hello there")
def lists(requests):
    # return HttpResponse("<H1>lists of products:</H1> ")
    page_obj=l=product.objects.all()
    product_names=requests.GET.get('search')
    if product_names != '' and product_names is not None:
        page_obj=product.objects.filter(name__icontains=product_names)
    paginator=Paginator(page_obj,6)
    page_number=requests.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # html = "<h1>List of Products:</h1><ol>"
    # for x in l:
    #     html += f"<li>{x}</li>"
    # html += "</ol>"
    context={
        "page_obj":page_obj
    }
    return render(requests,'myapp/index2.html',context)
# class based list veiw
class ProductListView(ListView):
    model=product  
    template_name='myapp/index2.html'
    context_object_name='products'
    paginate_by = 3
    

class ProductDetailView(DetailView):
    model=product  
    template_name='myapp/detail.html'
    context_object_name='item'
    def get_context_data(self,**kwargs) :
        context=super().get_context_data()
        context['stripe_key']=settings.STRIPE_PUBLISHABLE_KEY
        return context
# def products_detail(requests,id):
#     item=product.objects.get(id=id)
#     context={
#         "item":item
#     }
#     return render(requests,'myapp/detail.html',context)
@login_required
def addproducts(requests):
    if requests.method=='POST':
        name=requests.POST.get('name')
        price=requests.POST.get('price')
        des=requests.POST.get('des')
        image=requests.FILES['upload']
        Product=product(seller_name=requests.user,name=name,price=price,des=des,image=image)
        Product.save()
        return redirect('myapp:lists')
    return render(requests,'myapp/addproducts.html')

@method_decorator(login_required, name='dispatch')    
class ProductCreateView(CreateView):
    model=product
    fields=['name','price','des','image']
    success_url = '/myapp/lists/'
    def form_valid(self, form):
        form.instance.seller_name = self.request.user 
        return super().form_valid(form)

def update_products(requests,id):
    a=product.objects.get(id=id)
    if requests.method=='POST':
        a.name=requests.POST.get('name')
        a.price=requests.POST.get('price')
        a.des=requests.POST.get('des')
        if requests.FILES.get("upload"):
            a.image=requests.FILES['upload']
        a.save()
        return redirect('myapp:lists')
    context={
        "item":a
    }
    return render(requests,'myapp/updateproduct.html',context)
class ProductUpdateView(UpdateView):
    model=product
    fields=['name','price','des','image']
    template_name_suffix='_update_form'
    success_url = '/myapp/lists/'
    def form_valid(self, form):
        form.instance.seller_name = self.request.user
        return super().form_valid(form)

def delete_products(requests,id):
    item=product.objects.get(id=id)
    if requests.method=='POST':
        item=product.objects.get(id=id)
        item.delete()
        return redirect('myapp:lists')
    context={
        "item":item
    }
    return render(requests,'myapp/delete.html',context)
class ProductDeleteView(DeleteView):
    model=product
    success_url = '/myapp/lists/my_listings/'

@login_required    
def my_listings(request):
    products=product.objects.filter(seller_name=request.user)
    context={
        "products":products
    }
    return render(request,'myapp/my_listings.html',context)


@csrf_exempt
def create_check_out_session(request, id):
    item = get_object_or_404(product, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price*10),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('myapp:success')
        ) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(
            reverse('myapp:failed')
        ),
    )
    order = orderdetails(customer_username=request.user.username, product=item, amount=int(item.price*10), stripe_payment_intent=checkout_session.id)
    order.save()
    return JsonResponse({'SessionId': checkout_session.id})



class PaymentSuccessView(TemplateView):
    template_name = 'myapp/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        order = get_object_or_404(orderdetails, stripe_payment_intent=session_id)
        order.stripe_payment_intent = checkout_session.payment_intent
        order.has_paid = True
        order.save()
        order.product.is_sold = True 
        order.product.save()
        return render(request, 'myapp/success.html')
class PaymentFailedView(TemplateView):
    template_name = 'myapp/failed.html'