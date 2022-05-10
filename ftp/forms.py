from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
	First_Name = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"First Name",
	}))

	Last_Name = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"Last Name",
	}))

	username = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"Username",
	}))

	email = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"email",
		"placeholder":"Email",
	}))
	
	password1 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"password",
		"placeholder":"Password..Min 8 characters",
	}))

	password2 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"password",
		"placeholder":"Re-enter Password",
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

class RenameDirForm(forms.Form):
	d_name = forms.CharField(max_length=20)

class RenameFileForm(forms.Form):
	d_name = forms.CharField(max_length=20)

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
			"class":"form-control form-control-user",
			"type":"text",
			"placeholder":"Username",
	}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
			"class":"form-control form-control-user",
			"type":"password",
			"placeholder":"Enter password",
	}))
    class Meta:
        model = User
        fields = ('username', 'password')

class ChangePasswordForm(forms.Form):
	user_name =forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"Enter Your Username",
	}))
	pass_word = forms.CharField(widget=forms.PasswordInput(attrs={
			"class":"form-control form-control-user",
			"type":"password",
			"placeholder":"Enter New password",
	}))
	# class Meta:
	# 	model = User
	# 	fields = ('username','password')
   
