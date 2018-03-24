from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Direction


class SignUpForm(UserCreationForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses exist.')
        return email

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    idNumber = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'idNumber', 'first_name', 'last_name', 'password1', 'password2', )


class DirectionForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text='Required')

    class Meta:
        model = Direction
        fields = ['name', 'createdBy']


class ProfileUpdate(forms.ModelForm):


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



