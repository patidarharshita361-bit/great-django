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
