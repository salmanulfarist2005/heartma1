from django import forms
from . models import Contact,Product
from django.forms import widgets
from .models import Banner, Testimonial, Blog, ProductCategory, Product, Contact,Checkout,Review

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ()
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control required", "placeholder": "Your name:"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control required email",
                    "placeholder": "Your email:",
                }
            ),
            "phone": forms.NumberInput(
                attrs={
                    "class": "form-control ",
                    "placeholder": "Enter your phone number:",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control required",
                    "placeholder": "Enter your subject:",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control required",
                    "rows": 5,
                    "placeholder": "Your message:",
                }
            ),
        }






class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'room', 'image', 'color']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'old_price', 'price', 'slug', 'zoom_image', 'description']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'old_price', 'price', 'slug', 'zoom_image','description']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        exclude = ("timestamp",)
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name *"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name*"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email *"}),
            "mobil": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Mobile *"}),
            "street_address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street Address *"}),
            "pincode": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Pincode *"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State *"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City *"}),       
         }
        

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['name', 'title', 'rating', 'text']

        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control form-control-sm dark:bg-gray-100 dark:bg-opacity-5 dark:text-white dark:border-gray-800'})
        self.fields['title'].widget.attrs.update({'class': 'form-control form-control-sm dark:bg-gray-100 dark:bg-opacity-5 dark:text-white dark:border-gray-800'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control form-control-sm dark:bg-gray-100 dark:bg-opacity-5 dark:text-white dark:border-gray-800'})
        self.fields['text'].widget.attrs.update({'class': 'form-control form-control-sm dark:bg-gray-100 dark:bg-opacity-5 dark:text-white dark:border-gray-800', 'rows': 5})
