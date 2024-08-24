from django import forms
from App_payment.models import BillingAddress

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address', 'zip_code', 'city','country']