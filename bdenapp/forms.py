from django import forms
from django.contrib.auth.models import User
from .models import PropertyImage, Property, Review, UserProfile
from django.core.validators import MinValueValidator, MaxValueValidator

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password',
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password',
    }), label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
            }),
        }
        help_texts = {
            'username': '',  
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        return cleaned_data
    

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['location', 'owner', 'price', 'category', 'typeChoice', 'description', 'isAvailable', 'picture', 'isPeerToPeer', 'provision']

# for multiple image upload
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
    

class PropertyImageForm(forms.Form):
    pass
class ReviewForm(forms.ModelForm):
    class Meta:
        model =  Review
        fields = ['rating', 'review_text']

    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'rating-input', 'min': 1, 'max': 5, 'required': True}),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

# the purchase form handler

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True, label="Email Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Email Message")
    receipt_pdf = forms.FileField(required=False, label="Upload Payment Receipt (PDF)")
