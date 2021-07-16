from django import forms
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms import fields


class passwordchange(PasswordChangeForm):
    old_password=forms.CharField(label_suffix='',label='old Password',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'old password'}))
    new_password1=forms.CharField(label_suffix='',label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control ','placeholder':'new password'}))
    new_password2=forms.CharField(label_suffix='',label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control ','placeholder':'confirm password'}))
    password = None
    class Meta:
        model = User

        fields = ['old_password','new_password1','new_password2']
        

class loginform(AuthenticationForm):
    username = forms.CharField(label='Username',label_suffix=' ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(label='Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password '}))

    class Meta:
        model = User
        fields=['username']

class resetform(forms.Form):
    username = forms.CharField(label='Username',label_suffix=' ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(label='Email',label_suffix=' ',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'User@gmail.com'}))

class newpasswordform(resetform):
    username = forms.CharField(label='Username',label_suffix=' ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = None
    password1 = forms.CharField(label='Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password '}))
    password2 = forms.CharField(label='confirm Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm your password '}))

class signupform(UserCreationForm):
    username = forms.CharField(label='Username',label_suffix=' ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(label='Email',label_suffix=' ',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'User@gmail.com'}))
    password1 = forms.CharField(label='Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password '}))
    password2 = forms.CharField(label='confirm Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm your password '}))

    class Meta:
        model = User
        fields = ['username','email']