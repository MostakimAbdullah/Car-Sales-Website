from django.shortcuts import render
from carapp.models import CarModel,BrandModel


def home(request, category_slug = None):     
    data = CarModel.objects.all()
    if category_slug is not None:
        brand = BrandModel.objects.get(slug = category_slug)
        data = CarModel.objects.filter(brand = brand)
    categories = BrandModel.objects.all()
    return render(request, 'home.html', {'data' : data, 'category' : categories})