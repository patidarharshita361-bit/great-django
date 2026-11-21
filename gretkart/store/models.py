from django.db import models
from category.models import category
from django.urls import reverse


# Create your models here.
class product(models.Model):
    product_name   = models.CharField(max_length=200,unique=True)
    slug           = models.SlugField(max_length=200,unique=True)
    description    = models.TextField(max_length=200,unique=True)
    price          = models.IntegerField()
    image          = models.ImageField(upload_to='photo/product')
    stock          = models.IntegerField()
    is_available   = models.BooleanField(default=True)
    category       = models.ForeignKey(category,on_delete=models.CASCADE)
    created_date   = models.DateTimeField(auto_now_add = True)
    modified_date  = models.DateTimeField(auto_now=True)  


    def get_url(self):
        return reverse('products_detail',args=[self.category.slug,self.slug])
    def __str__(self):
       return self.product_name
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)      
Variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
    
class Variation(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=Variation_category_choice)  
    variation_value    = models.CharField(max_length=100)  
    is_active          = models.BooleanField(max_length=100)
    created            = models.DateTimeField(auto_now=True)


    objects = VariationManager()

    def __str__(self):
     return f"{self.product} - {self.variation_category}: {self.variation_value}"