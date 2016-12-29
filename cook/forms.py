from django.contrib.auth.models import User
from django import forms
from .models import Profile, Recipe, Review, Report, Rep_Image

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['introduction']

class RecipeForm(forms.ModelForm):

    servings = forms.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Recipe
        fields = ['title', 'servings', 'steps']

class ReviewForm(forms.ModelForm):

    rating = forms.IntegerField()

    class Meta:
        model = Review
        fields = ['title', 'text', 'suggestion', 'rating']

class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['description']

class ImageForm(forms.ModelForm):

    img = forms.FileField(label='img')

    class Meta:
        model = Rep_Image
        fields = ['img']
