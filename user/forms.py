from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserPermission

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            user= super(UserRegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user
