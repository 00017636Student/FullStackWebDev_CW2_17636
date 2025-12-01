from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BaseStyledForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

class BaseStyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()


class CustomUserCreationForm(BaseStyledModelForm, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': None
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class CustomLoginForm(BaseStyledForm, AuthenticationForm):
    class Meta:
        username = forms.CharField(label="Username")
        password = forms.CharField(label="Password", widget=forms.PasswordInput())