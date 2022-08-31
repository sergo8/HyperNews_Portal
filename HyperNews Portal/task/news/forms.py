from django import forms


class CreateNewsForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()


class SearchNewsForm(forms.Form):
    q = forms.CharField()