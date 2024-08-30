from django.db import models

# Create your models here.
class BrandModel(models.Model):
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    def __str__(self):
        return self.brand_name


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    quantity = models.IntegerField(blank = True, null = True)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/uploads/', blank = True, null = True)
    def __str__(self):
        return self.name


class Comments(models.Model):
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commented By {self.name}'