from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Паролі не співпадають. Будь ласка, введіть однакові паролі.'),
    }

    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label=_('Ім\'я'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label=_('Прізвище'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label=_('Телефон'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label=_('Підтвердження паролю'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Користувач з таким email вже існує'))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise ValidationError(_('Телефон повинен містити тільки цифри'))
        return phone



class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': _('Введіть правильну email-адресу')}
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    error_messages = {
        'invalid_login': _('Невірний email або пароль.'),
        'inactive': _('Ваш акаунт заблоковано. Зверніться до адміністратора.'),
    }

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if email:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    raise ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
            except User.DoesNotExist:
                pass

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )

        return self.cleaned_data

    def get_user(self):
        return self.user_cache