from django.contrib import admin
from . models import Banner,Testimonial,Blog,Product,ProductCategory,Contact,Checkout, OtherImages,Review,Logo,Offer
# Register your models here.
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug":("title",)}


class OtherImagesInline(admin.TabularInline):
    model = OtherImages
    fields = ("image","image_zoom")
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OtherImagesInline]
    list_display = ('name', 'category', 'price')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('first_name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating',)


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('logo',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title',)