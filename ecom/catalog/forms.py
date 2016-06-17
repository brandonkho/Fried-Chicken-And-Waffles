from django import forms
from catalog.models import Product

class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class':'quantity'}), 
                                  error_messages={'invalid':'Please enter a valid quantity.'}, 
                                  min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, request=None, *args, **kwargs):
        """ override the default so we can set the request """
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)
    