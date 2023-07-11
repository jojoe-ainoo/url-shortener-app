from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(required=True, max_length=255)
    hashed_url = forms.CharField(required=False, max_length=10)



"""
Form page to retrieve URL with pin
@param single filed for pin
"""
class PinForm(forms.Form):
    pin = forms.CharField(required=True,max_length=6)