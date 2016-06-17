from django.conf.urls import *

urlpatterns = patterns('cart.views', (r'^$', 'show_cart', { 'template_name': 'cart/cart.html' }, 'show_cart'),
)