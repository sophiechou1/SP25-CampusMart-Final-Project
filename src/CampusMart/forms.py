from django import forms

class PurchaseListingsForm(forms.Form):
    number_of_listings = forms.IntegerField(min_value=1, label="Number of Listings to Purchase")