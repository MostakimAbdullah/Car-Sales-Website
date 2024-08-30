from django.contrib import admin
from carapp.models import CarModel,BrandModel,Comments
# Register your models here.
admin.site.register(CarModel)

class CarBrandModel(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('brand_name',)}
    list_display = ['brand_name', 'slug']

admin.site.register(BrandModel, CarBrandModel)

admin.site.register(Comments)