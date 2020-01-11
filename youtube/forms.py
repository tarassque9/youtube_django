from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='your_name', max_length=30)
    password = forms.CharField(label='your_password', max_length=30)

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password', max_length=30)
    email = forms.CharField(label='email', max_length=30)

class CommentForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)
    video = forms.HiddenInput()

class NewVideoForm(forms.Form):
    title = forms.CharField(label='title', max_length=30)
    description = forms.CharField(label='description', max_length=300)
    file = forms.FileField()