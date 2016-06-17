from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=29.99)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('catalog_product', kwargs={"product_slug": self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to="catalog/images")
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.product.title

    def __str__(self):
        return self.product.title