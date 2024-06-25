from decimal import Decimal
from typing import Any
import urllib.parse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView,CreateView
from django.views.generic import DetailView
from django.urls import reverse, reverse_lazy
from . models import Banner,Testimonial,Blog,Product, ProductCategory,Wishlist
from django.shortcuts import render, get_object_or_404
from .models import Product,Offer
from django.views.generic import View, RedirectView
from django.contrib.auth import authenticate, login
from .forms import LoginForm,ContactForm,CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .cart import Cart

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Banner,Review
from .forms import BannerForm,ProductForm,ReviewForm
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('web:dashboard')
    else:
        form = LoginForm()
    return render(request, 'web/dashboard/login.html', {'form': form})




class IndexView(TemplateView):
    template_name = 'web/index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = Banner.objects.all()
        blogs = Blog.objects.all()[:3]
        products = Product.objects.all()
        offers = Offer.objects.all()
        reviews = Review.objects.all()  # Fetch all reviews
        categories = ProductCategory.objects.all()[:10]

        context["banners"] = banners
        context["blogs"] = blogs
        context["products"] = products
        context["categories"] = categories
        context["offers"] = offers
        context["reviews"] = reviews
        
        # Group products by category
        category_products = {
            category: products.filter(category=category) for category in categories
        }
        context["category_products"] = category_products

        return context

    

class AboutView(TemplateView):

    template_name = 'web/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        testimonials = Testimonial.objects.all()
        categories = ProductCategory.objects.all()
        context["categories"] = categories
        context["testimonials"] = testimonials
        
        return context

def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully updated",
            }
            return JsonResponse(response_data)
        else:
            print(form.errors)
            response_data = {"status": "false", "title": "Form validation error"}
            return JsonResponse(response_data)
    else:
        initial_data = {'interest': 'dealership'}  # Define your initial data here
        form = CheckoutForm(initial=initial_data)  # Pass initial data to the form

        # Fetch product categories and testimonials
        categories = ProductCategory.objects.all()

        context = {
            "form": form,
            "categories": categories,  # Add categories to the context
        }
        return render(request, "web/checkout.html", context)


class ContactView(TemplateView):
    template_name = 'web/contact.html'  


class ContactusView(TemplateView):
    template_name = 'web/dashboard/contact-us.html'  


class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.all()
        context["categories"] = categories
        return context


class AddToWishlistView( View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(Product, pk=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            # Create a new Wishlist object
            Wishlist.objects.create(
                user=user,
                product=product
            )
            return JsonResponse({'message': 'Product Added from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.','alreadyInWishlist': True})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, product_id=product_id)
        wishlist_item.delete()

        return redirect("web:wishlist")




    


class BlogListView(TemplateView):
    template_name = 'web/blog_list.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs   = Blog.objects.all()
        categories = ProductCategory.objects.all()

        context["categories"] = categories
        context["blogs"] = blogs
        return context

class ProductsListView(ListView):
    model = Product
    template_name = 'web/products_list.html'
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        
        # Fetch all reviews and add to the context
        context['reviews'] = Review.objects.all()
        
        return context



# class ProductsAddlView(CreateView):
#     model = Product 
#     template_name = 'web/products.html'
#     fields = ['name', 'description', 'price', 'category']
#     success_url = reverse_lazy("web:cart.html")




# class ProductDetailView(TemplateView):
#     template_name = 'web/product_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = self.kwargs.get('slug')
#         products = get_object_or_404(Product, slug=slug)
#         categories = ProductCategory.objects.all()
        
#         other_products = Product.objects.exclude(slug=slug)
#         context['products'] = products
#         context['other_products'] = other_products
#         context["categories"] = categories
        
#         return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "web/product_detail.html"
    context_object_name = "product"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['other_products'] = Product.objects.exclude(slug=product.slug)
        context['form'] = ReviewForm()
        
        # Fetch reviews related to the product
        context['reviews'] = product.reviews.filter(is_active=True).order_by('-created_at')
        
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Review successfully submitted",
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "errors": form.errors,
            }
            print(form.errors)
            return JsonResponse(response_data, status=400)
        

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context)
         
      



class BlogDetailView(DetailView):
    model = Blog
    template_name = 'web/blog-detail.html'  # Assuming you have a template for blog detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.all()
        slug = self.kwargs.get('slug')  # Get slug from URL parameters
        blogs = get_object_or_404(Blog, slug=slug)
        categories = ProductCategory.objects.all()
        other_blogs = Blog.objects.exclude(slug=slug)

        context["blogs"] = blogs
        context['other_blogs'] = other_blogs
        context["categories"] = categories

        return context


class ProductCategoryListView(TemplateView):
    template_name = 'web/product-category.html'


class DashboardView(LoginRequiredMixin,TemplateView ):
    template_name = 'web/dashboard/dashboard.html'
   

class categorylistdView(TemplateView):
    template_name = 'web/dashboard/category-list.html'



class CartView(TemplateView):
    template_name = 'web/cart.html'


class AddProductAdminView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'web/dashboard/add_product.html'
    fields = ['category','name','image','old_price','price','description']
    success_url = reverse_lazy("web:dashboard")


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'web/dashboard/product_list.html'
    context_object_name = "products"



def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            # Build the WhatsApp message
            message = (
                f'Name: {form.cleaned_data["name"]} \n'
                f'Email: {form.cleaned_data["email"]}\n'
                f'Phone: {form.cleaned_data["phone"]}\n'
                f'Subject: {form.cleaned_data["subject"]}\n'
                f'Message: {form.cleaned_data["message"]}\n'
            )

            whatsapp_api_url = "https://api.whatsapp.com/send"
            phone_number = "+917909131871"
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = (
                f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"
            )

            # Redirect to the WhatsApp link
            return redirect(whatsapp_url)

        else:
            error_messages = {field: form.errors[field][0] for field in form.errors}
            print("Form Validation Error:", error_messages)  # Print the errors
            response_data = {
                "status": "false",
                "title": "Form Validation Error",
                "message": error_messages,
            }
            return JsonResponse(response_data)

    else:
        form = ContactForm()

    # Fetch product categories and testimonials
    categories = ProductCategory.objects.all()


    context = {
        "form": form,
        "categories": categories,  # Add categories to the context

    }
    return render(request, "web/contact.html", context)


class FAQView(TemplateView):
    template_name = 'web/faq.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.all()
        context["categories"] = categories

        return context

def banner_form(request):
    return render(request,'dashboard/banner_form.html' )




class BannerListView(ListView):
    model = Banner
    template_name = 'web/dashboard/banner_list.html'
    context_object_name = 'banners'


class BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'web/dashboard/banner_form.html'
    success_url = reverse_lazy('web:banner_list')


class BannerUpdateView(UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'web/dashboard/banner_form.html'
    success_url = reverse_lazy('web:banner_list')


class BannerDeleteView(DeleteView):
    model = Banner
    template_name = 'web/dashboard/banner_confirm_delete.html'
    success_url = reverse_lazy('web:banner_list')
    context_object_name = 'banner'



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'web/dashboard/product_form.html'
    success_url = reverse_lazy('web:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'web/dashboard/product_form.html'
    success_url = reverse_lazy('web:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'web/dashboard/product_confirm_delete.html'
    success_url = reverse_lazy('web:product_list')
    context_object_name = 'product'


class ProductListView(ListView):
    model = Product
    template_name = 'web/dashboard/product_list.html'
    context_object_name = 'products'



class ProductListView(ListView):
    model = Product
    template_name = 'web/dashboard/product_listedd.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'web/dashboard/product_form.html'
    success_url = reverse_lazy('web:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'web/dashboard/product_form.html'
    success_url = reverse_lazy('web:product_list')

class ProductDeleteView(DeleteView):
    model = Product,
    template_name = 'web/dashboard/product_confirm_delete.html'
    success_url = reverse_lazy('web:product_list')
    context_object_name = 'product'


#cart
    
class CartView(View):
    def get(self, request):
        cart = Cart(request)
        cart_items = []

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(Product, id=item_id)
            quantity = item_data['quantity']
            total_price = Decimal(item_data['price']) * quantity
            
            cart_items.append({
                'product': variant,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Fetch product categories and testimonials
        categories = ProductCategory.objects.all()
      
        context = {
            'cart_items': cart_items,
            'cart_total': cart.cart_total(),
            'categories': categories,  # Add categories to the context
        }

        return render(request, "web/cart.html", context)


class CartAddView(View):
    def get(self, request):
        cart = Cart(request)
        cart_instance = cart.cart
        quantity = request.GET.get('quantity', 1)
        product_id = request.GET.get("product_id", '')
        price = request.GET.get("price", None)
        variant = get_object_or_404(Product, pk=product_id)
        cart.add(variant, quantity=int(quantity),price=price)
        
       
        return JsonResponse({
            'quantity': cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[product_id]),  
            'cart_total': cart.cart_total(),
            'cart_count': len(cart_instance),
            
        })
    
    
class ClearCartItemView(View):
    def get(self, request, item_id):
        cart = Cart(request)
        variant = get_object_or_404(Product, id=item_id)
        cart.remove(variant)
        return redirect('web:cart')


class MinusToCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart_instance = cart.cart
        item_id = request.GET.get("item_id")
        variant = get_object_or_404(Product, id=item_id)
        cart.decrease_quantity(variant)
        return JsonResponse({
            'quantity':cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[item_id]),
            'cart_total': cart.cart_total(),
        })
    

class ClearCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect(reverse('web:index'))