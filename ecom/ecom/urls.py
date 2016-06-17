from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
#from ecom.c
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'catalog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^catalog/', 'catalog.views.all', name='catalog'),

    url(r'^admin/', include(admin.site.urls)),

    #url(r'^cart/', include('cart.urls')),

    url(r'^cart/$', 'cart.views.show_cart', name='show_cart'),

    #url(r'^catalog/', include('catalog.urls')),

    url(r'^catalog/$', 'catalog.views.all', name='catalog_home'),

    url(r'^catalog/product/(?P<product_slug>[-\w]+)/$', 'catalog.views.show_product', name='catalog_product')
    #(r'^product/(?P<product_slug>[-\w]+)/$', 'show_product', { 'template_name':'catalog/product.html'},'catalog_product'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
