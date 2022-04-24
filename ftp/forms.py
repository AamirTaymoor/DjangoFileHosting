from cProfile import label
from dataclasses import field, fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
	First_Name = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"text",
		"placeholder":"enter Firstname",
	}))

	Last_Name = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"text",
		"placeholder":"enter Last name",
	}))

	username = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"text",
		"placeholder":"enter Username",
	}), label="Username")

	email = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"email",
		"placeholder":"enter email id",
	}))
	
	password1 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"password",
		"placeholder":"enter password",
	}))

	password2 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"input",
		"type":"password",
		"placeholder":"re-enter password",
	}))

	class Meta:
		model = User
		fields = ("First_Name","Last_Name", "username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=True)
		user.email = self.cleaned_data['email']
		user.First_Name = self.cleaned_data['First_Name']
		user.Last_Name = self.cleaned_data['Last_Name']
		if commit:
			user.save()
		return user

class FileUpload(forms.Form):
	file = forms.FileField(label= 'Select a file')

class CreateDirForm(forms.Form):
   d_name = forms.CharField(max_length = 100)

class UserLoginForm(AuthenticationForm):
    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control form-control-user", 
		"type":"validate",
		"placeholder": "Username",
		"id":"exampleInputEmail"
	}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control form-control-user",
		"type":"password",
		"placeholder":"Enter password",
		"id":"exampleInputPassword"
	}))
    class Meta:
         model = User
         fields = ('username', 'password')
         #AuthenticationFormFields = ('username', 'password')
        #  exclude = []


	