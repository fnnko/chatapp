from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    pass

# 以下を追加
class Talk(models.Model):
    # メッセージ
    message = models.CharField(max_length=500)
    # 送信者
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_talk"
    )
    # 受信者
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_talk"
    )
    # 時刻
    # auto_now_add=True とすると、そのフィールドの値には、オブジェクトが生成されたときの時刻が保存されます。
    time = models.DateTimeField(auto_now_add=True)

    def get_elapsed_time(self):
        delta = timezone.now() - self.time

        zero = timedelta()
        one_hour = timedelta(hours=1)
        one_day = timedelta(days=1)
        one_week = timedelta(days=7)

        if delta < zero:
            raise ValueError("未来の時刻です。")

        if delta < one_hour:
            return f"{delta.seconds // 60} 分前"
        
        elif delta < one_day:
            return f"{delta.seconds // 3600} 時間前"

        elif delta < one_week:
            return f"{delta.days} 日前"

        else:
            return "1 週間以上前"



    def __str__(self):
        return "{} -> {}".format(self.sender, self.receiver)
