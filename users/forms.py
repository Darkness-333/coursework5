from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)  # Без требований к паролю
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput,
                                required=False)  # Без требований к паролю

    # Убираем подсказку для поля 'username'
    username = forms.CharField(
        label='Username',
        help_text=''  # Убираем подсказку
    )
    class Meta:
        model = CustomUser
        # fields = ('username', 'email', 'role', 'password1', 'password2')
        fields = ('username', 'role')
