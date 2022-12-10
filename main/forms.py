from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .models import Talk, User

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("message",)

# 以下を追加
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}
        help_texts = {"username": ""}

class EmailChangeForm(forms.ModelForm):
    class Meta:
        # ここに、「model = User」が抜けてる！
        # model = User ：このフォームが、Userというデータベースと紐づいていることを示す
        # このフォームによって、Userのemailという項目を更新したいので、ここが必要！
        model = User
        fields = ("email",)
        labels = {"email":"新しいメールアドレス"}
        help_texts ={"email":""}

