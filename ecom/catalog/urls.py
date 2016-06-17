from django.conf.urls import *

urlpatterns = patterns('views',
(r'^$', 'all', { 'template_name':'catalog/menu.html'}, 'catalog_home'),
(r'^product/(?P<product_slug>[-\w]+)/$', 'show_product', { 'template_name':'catalog/product.html'},'catalog_product'),
)