from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models.functions import Concat
import json
from django.db.models import Avg, Count, Q, F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from mystore.models import Category, Product, Images, Variants

from home.forms import SearchForm

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "index.html", {'products':products, 'categories':categories,})


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request,
#                   'shop/product/store.html',
#                   {'category': category,
#                    'categories': categories,
#                    'products': products})

# def product_detail(request, id, slug):

#     product = Product.objects.get(pk=id)
#     images = Images.objects.filter(product_id=id)
#     # product = Product.objects.get(pk=id)
#     context = {'product': product,
#                'images': images,
#                }
#     if product.variant !="None": # Product have variants
#         if request.method == 'POST': #if we select color
#             variant_id = request.POST.get('variantid')
#             variant = Variants.objects.get(id=variant_id) #selected product by click color radio
#             colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
#             sizes = Variants.objects.raw('SELECT * FROM  mystore_variants  WHERE product_id=%s GROUP BY size_id',[id])
            
#         else:
#             variants = Variants.objects.filter(product_id=id)
#             colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
#             sizes = Variants.objects.raw('SELECT * FROM  mystore_variants  WHERE product_id=%s GROUP BY size_id',[id])
#             variant =Variants.objects.get(id=variants[0].id)
#         context.update({'sizes': sizes, 'colors': colors,
#                         'variant': variant
#                         })
#     return render(request,
#                   'shop/product/detail.html', context  )


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('shop/product/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            products = Product.objects.filter(name__icontains=query)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'shop/product/search_products.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.name +" > " + rs.category.name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)