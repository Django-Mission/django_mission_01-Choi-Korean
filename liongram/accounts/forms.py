from dataclasses import field, fields
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm  # 장고에서 제공하는 기본 회원가입 폼


class UserBaseForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class UserCreateForm(UserBaseForm):
    password2 = forms.CharField(widget=forms.PasswordInput) # 비밀번호 확인용 두번째 칸
    class Meta(UserBaseForm.Meta):
        fields = ['username', 'email', 'phone', 'password']

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email']