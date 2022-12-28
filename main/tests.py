from django.test import TestCase

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .forms import TalkForm
from .models import Talk,User

class TestTalkModel(TestCase):  # TestCase を継承するのを忘れないように。
    @classmethod
    def setUpClass(cls):
        # Talk モデルのテストで使用する変数の初期化をしています。
        super().setUpClass()
        now = timezone.now()
        cls._talk_30minutes_ago = Talk(time=now - timedelta(minutes=30))
        cls._talk_3hours_ago = Talk(time=now - timedelta(hours=3))
        cls._talk_3days_ago = Talk(time=now - timedelta(days=3))
        cls._talk_9days_ago = Talk(time=now - timedelta(days=9))
        cls._talk_3weeks_ago = Talk(time=now - timedelta(weeks=3))
        cls._talk_future = Talk(time=now + timedelta(weeks=3))

    def test_valid_elapsed_time(self):
        self.assertEqual(self._talk_30minutes_ago.get_elapsed_time(), "30 分前")
        self.assertEqual(self._talk_3hours_ago.get_elapsed_time(), "3 時間前")
        self.assertEqual(self._talk_3days_ago.get_elapsed_time(), "3 日前")
        self.assertEqual(self._talk_9days_ago.get_elapsed_time(), "1 週間以上前")
        self.assertEqual(self._talk_3weeks_ago.get_elapsed_time(), "1 週間以上前")

    def test_invalid_elapsed_time(self):
        with self.assertRaises(ValueError):
            self._talk_future.get_elapsed_time()

# Create your tests here.

class TestTalkForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # フォームはコンストラクタの引数に辞書を渡すことで初期化することができます。
        cls._good_form = TalkForm({"message": "こんにちは今日もプログラミングを頑張るぞ"})
        cls._bad_form1 = TalkForm({"message": "君はあほだね"})
        cls._bad_form2 = TalkForm({"message": "彼はバカというよりかはあほだ"})

    def test_good_talk(self):
        self.assertTrue(self._good_form.is_valid())

    def test_bad_talk(self):
        self.assertFalse(self._bad_form1.is_valid())
        self.assertIn("禁止ワード あほ が含まれています", self._bad_form1.errors["message"])

        self.assertFalse(self._bad_form2.is_valid())
        self.assertIn(
            "禁止ワード バカ, あほ が含まれています", self._bad_form2.errors["message"]
        )

class TestSignupView(TestCase):
    def test_get(self):
        # GET 時のテスト
        res = self.client.get("/signup/")
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/signup.html")

    def test_valid_post(self):
        data = {
            "username": "test太郎",
            "email": "test@example.com",
            "password1": "thisistest",
            "password2": "thisistest",
        }
        # POST 時のデータは辞書にして渡します。
        res = self.client.post("/signup/", data)
        # Django のリダイレクトを検証します。
        # リダイレクト時のステータスコードは 302
        self.assertRedirects(
            res,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_invalid_post(self):
        # 不正な入力
        params = {
            "username": "test",
            "email": "メールアドレス",
            "password1": "thisistest",
            "password2": "thisistest",
        }
        res = self.client.post("/signup/", params)
        self.assertEqual(res.status_code, 200)
        # レンダリングに使用されるテンプレートの検証をしています。
        self.assertTemplateUsed(res, "main/signup.html")

class TestWithAuthMixin:
    """ログインが必要なテストクラスで継承する"""

    @classmethod
    def setUpTestData(cls):
        # ログインする前にデータベースにテスターを登録しておく必要がある。
        cls._username = "test太郎"
        cls._email = "test@example.com"
        cls._password = "thisistest"
        cls.user = User.objects.create_user(
            username=cls._username, email=cls._email, password=cls._password
        )

    def login(self):
        return self.client.login(
            username=self._username, password=self._password
        )

class TestTalkRoomView(TestWithAuthMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._good_form = {"message": "こんにちは今日もプログラミングを頑張るぞ"}
        cls._bad_form = {"message": "彼はバカというよりかはあほだ"}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._friend_username = "friend太郎"
        cls._friend_email = "friend@example.com"
        cls._friend_password = "thisistest"
        cls._friend = User.objects.create_user(
            username=cls._friend_username,
            email=cls._friend_email,
            password=cls._friend_password,
        )
        cls._talk_room_url = f"/talk_room/{cls._friend.id}"

    def test_get(self):
        self.login()
        res = self.client.get(self._talk_room_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/talk_room.html")

    def test_valid_post(self):
        self.login()
        res = self.client.post(self._talk_room_url, self._good_form)
        self.assertRedirects(
            res,
            self._talk_room_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_invalid_post(self):
        self.login()
        res = self.client.post(self._talk_room_url, self._bad_form)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/talk_room.html")
        # レンダリングされたテンプレートに第二引数の文字列が含まれるかを検証。
        self.assertContains(res, "禁止ワード バカ, あほ が含まれています")``