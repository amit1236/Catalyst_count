from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


class QueryForm(forms.Form):
    industry = forms.CharField(max_length=100, required=False)
    min_revenue = forms.DecimalField(max_digits=15, decimal_places=2, required=False)
    max_revenue = forms.DecimalField(max_digits=15, decimal_places=2, required=False)
    locality = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    employees_from = forms.IntegerField(required=False)
    employees_to = forms.IntegerField(required=False)