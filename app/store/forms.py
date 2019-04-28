from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='eg. yoursemail@anyemail.com')

    class Meta:
        model = User
        # password1, password2 는 UserCreationForm 에 있기 때문에 따로 정의하지 않고도 fields 에서 사용 가능
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
