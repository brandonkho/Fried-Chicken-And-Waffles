from django.shortcuts import render, get_object_or_404

# Create your views here.
from .forms import ProductAddToCartForm
from .models import Product
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from cart import cart

def home(request):
	if request.user.is_authenticated():
		username_is = "Jamal"
		context = {"username_is": request.user}
	else:
		context = {"username_is": request.user}
	
	template = 'base.html'	
	return render(request, template, context)

def all(request):
    products = Product.objects.all()
    context = {'products': products}
    template = 'catalog/menu.html'  
    return render(request, template, context)


def show_product(request, product_slug):
    template_name="catalog/product.html"
    print(product_slug)
    p = get_object_or_404(Product, slug=product_slug)
    page_title = p.title
    # evaluate the HTTP method, change as needed
    if request.method == 'POST':
        #create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        #check if posted data is valid
        if form.is_valid():
            #add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        #create the unbound form. Notice the request as a keyword argument
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set test cookie to make sure cookies are enabled
    request.session.set_test_cookie()
    #return render_to_response(template_name, locals(), context_instance=RequestContext(request))

    context = {'p': p, 'page_title': p.title, 'form': form}
    return render(request, template_name, context)