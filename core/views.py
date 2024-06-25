from django.urls import reverse_lazy

from core import mixins


class HomeView(mixins.TemplateView):
    
    template_name = "core/home.html"

     
    
