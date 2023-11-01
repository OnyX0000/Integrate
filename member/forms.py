from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class NewProfileChangeForm(UserChangeForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # 비밀번호 해싱하여 저장
        if commit:
            user.save()
        return user
