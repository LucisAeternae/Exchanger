from django import forms
from baseapp.models import CustomUser, Profile, Offer, Game, Category

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
    field_order = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar',]

class BaseOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'description', 'price', 'type')
    field_order = ('title', 'description', 'price', 'type')

class CustomOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('quantity', 'rangestep')
    field_order = ('quantity', 'rangestep')

class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'description', 'logo')
    field_order = ('name', 'description', 'logo')

class NewCategoryForm(forms.ModelForm):
    game = forms.ModelChoiceField(queryset=Game.objects.all())
    class Meta:
        model = Category
        fields = ('title', 'game')
    field_order = ('name', 'game')
