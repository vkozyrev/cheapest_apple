# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.core import serializers

from cheapest_apple.cheapestapple.models import Box, Product, Price, Store

ROWS = 3

def index(request):
    return render_to_response('cheapestapple/index2.html')

def sara(request):
    return HttpResponse("Hi SARA!!!! -Vlad")

def noJSindex(request, page_id, type):
    if type == 'box':
        parent = Box.objects.get(id=page_id)
        child_set = parent.child.all()
        height = ((child_set.count() / ROWS) * 320) + 100
        if child_set.count() % ROWS != 0:
            height = height + 320;
        return render_to_response('cheapestapple/index.html', {'parent': parent, 'child_set': child_set, 'height': height})
    if type == 'product':
        parent = Box.objects.get(id=page_id)
        child_set = parent.product_box.all()
        height = ((child_set.count()) * 170) + 120
        return render_to_response('cheapestapple/product.html', {'parent': parent, 'child_set': child_set, 'height': height})
    if type == 'price':
        parent = Product.objects.get(id=page_id)
        child_set = parent.prices.all().order_by('price')
        review_set = parent.reviews.all().order_by('-score')
        height = ((child_set.count()) * 110) + 340
        price_height = 0
        review_height = 0
        return render_to_response('cheapestapple/price.html', {'parent': parent, 'child_set': child_set, 'height': height, 
                                                               'review_set': review_set, 'price_heigh': price_height, 
                                                               'review_height': review_height})
    else:
        raise Http404()

def getTree(request):
    if request.method == 'POST':
        querySet = Box.objects.all();
        jsonSerializer = serializers.get_serializer("json")()
        return HttpResponse(jsonSerializer.serialize(querySet))
    return HttpResponse('ERROR!')

def getProducts(request):
    if request.method == 'POST':
        querySet = Product.objects.all();
        jsonSerializer = serializers.get_serializer("json")()
        return HttpResponse(jsonSerializer.serialize(querySet))
    return HttpResponse('ERROR!')

def getPrices(request):
    if request.method == 'POST':
        querySet = Price.objects.all();
        jsonSerializer = serializers.get_serializer("json")()
        return HttpResponse(jsonSerializer.serialize(querySet))
    return HttpResponse('ERROR!')
