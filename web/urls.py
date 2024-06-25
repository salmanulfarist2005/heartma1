from django.contrib import admin
from django.urls import path,include
from . import views 
from .views import ProductDetailView
# from .views import cart_view, add_to_cart, remove_from_cart, update_cart_item
from .views import BannerListView, BannerCreateView, BannerUpdateView, BannerDeleteView, WishlistListView,ProductListView,ProductCreateView,ProductUpdateView,ProductDeleteView

app_name = 'web'


urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("about/", views.AboutView.as_view(), name="about"),
     path('checkout/', views.checkout, name='checkout'),
    path("contact/",views.contact,name='contact'),
    
    path("blog/", views.BlogListView.as_view(), name="blog"),
    path('blog/<slug:slug>/',views.BlogDetailView.as_view(), name='blog-detail'),
    path("product-category/", views.ProductCategoryListView.as_view(), name="product_category"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path("contact-us/", views.ContactusView.as_view(), name="contact-us"),
    path('category-list/', views.categorylistdView.as_view(), name='category-list'),
    # path('products/', views.ProductsAddlView.as_view(), name='add_products'),
    path("product_list/",views.ProductsListView.as_view(), name="product_list"),
    path('product-detail/<slug:slug>/',ProductDetailView.as_view(), name='product_detail'),
    path('login/', views.user_login, name='login'),    
    path("admin-dashboard/product/add/", views.AddProductAdminView.as_view(), name="add_product"),
    path("admin-dashboard/product/list/", views.ProductListView.as_view(), name="list_product"),
    path("faq/",views.FAQView.as_view(), name='faq'),
    #dashbord
    path('banners/from/', views.banner_form, name='banner_form'),
    path('banners/', BannerListView.as_view(), name='banner_list'),
    path('banners/new/', BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/edit/', BannerUpdateView.as_view(), name='banner_update'),
    path('banners/<int:pk>/delete/', BannerDeleteView.as_view(), name='banner_delete'),
    # dashbord_product
    # Product URLs

    # path('products/', ProductListView.as_view(), name='product_list'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path("admin-dashboard/product/list/", views.ProductListView.as_view(), name="product_listedd"),
    #cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartAddView.as_view(), name='add_cart'),
    path('cart-item-clear/<str:item_id>/', views.ClearCartItemView.as_view(), name='clear_cart_item'),
    path('cart/minus/', views.MinusToCartView.as_view(), name='minus_to_cart'),
    path('cart-clear/', views.ClearCartView.as_view(), name='clear_cart'),
    #wishlist
    path("wishlist/", views.WishlistListView.as_view(), name="wishlist"),
    path("wishlist/add/",views.AddToWishlistView.as_view(),name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/",views.RemoveFromWishlistView.as_view(),name="remove_from_wishlist"),
   
]




