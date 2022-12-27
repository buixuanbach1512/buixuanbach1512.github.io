from django import forms

class registerForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class loginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)