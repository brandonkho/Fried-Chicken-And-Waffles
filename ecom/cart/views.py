from django.shortcuts import render, get_object_or_404

# Create your views here.
from cart import cart

def show_cart(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart' 
    cart_subtotal = cart.cart_subtotal(request)
    context = {'cart_items': cart_items, 'page_title': page_title, 'cart_subtotal': cart_subtotal}
    template_name = 'cart/cart.html'
    #return render_to_response(template_name, locals(), context_instance=RequestContext(request))

    return render(request, template_name, context)