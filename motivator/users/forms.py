from django import forms
from django.contrib.auth.forms import UserCreationForm   # type: ignore
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class MotivationCreateForm(forms.Form):
    motivation = forms.CharField(widget =forms.Textarea(attrs={
            'class': 'form-control mt-4',
            'placeholder': 'Напишите свою мотивацию.'
                    }))