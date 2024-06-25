from datetime import timezone
import uuid
from django.db import models
from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from colorfield.fields import ColorField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Logo(models.Model):
    logo = models.ImageField(upload_to='logo/')

class Offer(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='offer/')


    def __str__(self):
      return self.title
  

# Create your models here.
class Banner(models.Model): 
   title = models.CharField(max_length=100)
   room = models.CharField(max_length=100)
   image = models.ImageField(upload_to='banner/')
   color = ColorField(default='#FF0000')


   def __str__(self):
      return self.title
 

class Testimonial(models.Model):
   name = models.CharField(max_length=100)
   position = models.CharField(max_length=100)
   image = models.ImageField(upload_to='testimonial/')
   description = models.TextField()


   def __str__(self):
       return self.name
   

class Blog(models.Model):
   title = models.CharField(max_length=200)
   image  = models.ImageField(upload_to='blog/')
   name = models.CharField(max_length=100)
   detiail_image = models.ImageField(upload_to='blog_detail/')
   date = models.DateField(blank=True,null=True)
   description = HTMLField()
   slug = models.SlugField(max_length=250,blank=True,null=True)

   def get_absolute_url(self):
        return reverse("web:blog-detail", kwargs={"slug": self.slug})
   
   def __str__(self):
       return self.name
   
class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category/')
    slug = models.SlugField(unique=True)

    def get_products(self):
        return Product.objects.filter(category=self)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(
        "web.ProductCategory",
        verbose_name="product Category",
        related_name="product_category",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    old_price = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()
    slug = models.SlugField(max_length=250, blank=True, null=True)
    zoom_image = models.ImageField(upload_to='zoom/')
    description = HTMLField()

    def get_image(self):
        return OtherImages.objects.filter(product=self)

    def get_absolute_url(self):
        return reverse("web:product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
    

class OtherImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/",blank=True,null=True)
    image_zoom = models.ImageField(upload_to='zoom/',blank=True,null=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200,blank=True,null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True,blank=True,null=True)
    rating = models.IntegerField()  # Rating out of 100
    text = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.rating} stars"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("web.Product", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.product}"



class Contact(models.Model):
    name  = models.CharField(max_length=100)  
    email  = models.EmailField()
    phone = models.IntegerField()
    subject = models.CharField(max_length=250)
    message  = models.TextField()


    def __str__(self):
        return self.name
    

class Checkout(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    mobil = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.CharField(max_length=100)
    email  = models.CharField(max_length=100)



class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_product_name(self):
        return self.product

    def get_total_price(self):
        res = float(self.quantity) * float(self.product.sale_price)
        return round(res,2)

    def cart_total(self):
        return float(sum(item.get_total_price() for item in Cart.objects.filter(user=self.user)))

    def _str_(self):
        return f"{self.product} - {self.quantity}"
    
def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]
    return f"{timestamp}{unique_id.upper()}"



  
