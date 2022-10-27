
# import from third party libraries
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# import from current project
from django import forms

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class MotivationCreateForm(forms.Form):
    motivation = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control mt-4',
            'placeholder': 'Напишите свою мотивацию.'
                    }))
