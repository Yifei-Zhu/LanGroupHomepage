from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Send a password reset email to a specific user.'

    def handle(self, *args, **options):
        users = User.objects.exclude(username__in=['lanzg', 'xuc'])
        #user = User.objects.get(username='zhuyf')

        for user in users:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://121.41.79.67:8000{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

            message = f"你好，{user.first_name} {user.last_name}。欢迎使用LanGroup Website，由于服务器限制无法备案，暂时只能使用IP访问（http://121.41.79.67:8000/）新用户请重置密码：{reset_url}。"

            send_mail(
                'Password Reset',
                message,
                'lan_group@outlook.com',
                [user.email],
                fail_silently=False,
            )

