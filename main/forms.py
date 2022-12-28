from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User,Talk

import logging

logger = logging.getLogger(__name__)

from django.core.mail import send_mail # 追加

TABOO_WORDS = [
    "ばか",
    "バカ",
    "あほ",
    "アホ",
    "キモイ",
    "きもい",
    "うんこ",

]


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

    def clean_message(self):
        message = self.cleaned_data["message"]
        matched = [w for w in TABOO_WORDS if w in message]
        if matched:

            logger.info("%sという禁止語が入力されました。",''.join(matched))

            # メール送信に必要な情報の設定
            email = "receiver@example.com"

            subject = "不適切な言葉の送信がありました。"
            message = "この文には%sという言葉が含まれています。" % (''.join(matched))
            from_email = "sender@example.com"  # 送信者のメールアドレス
            recipient_list = [email]  # 受信者のメールアドレス
            send_mail(subject, message, from_email, recipient_list)

            raise ValidationError(f"禁止ワード {', '.join(matched)} が含まれています")  
        return message

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

