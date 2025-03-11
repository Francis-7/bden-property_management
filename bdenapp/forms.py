from django import forms
from django.contrib.auth.models import User
from .models import PropertyImage, Property, Review, UserProfile

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
        fields = '__all__'

class PropertyImageForm(forms.ModelForm):
    # image = forms.FileField(widget=forms.TextInput(attrs={"name":"images","type":"File","multiple":"True"}), label = "Upload Images")
    class Meta:
        model = PropertyImage
        fields = ['property', 'images']
        property = forms.CharField(widget=forms.TextInput(attrs={'name':'property'}), label='Property')
        images = forms.FileField(widget=forms.TextInput(attrs={"name":"images","type":"File","multiple":"True"}), label = "Upload Images")
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model =  Review
        fields = ['rating', 'review_text']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']