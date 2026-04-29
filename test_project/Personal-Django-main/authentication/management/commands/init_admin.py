from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Initialize admin user'

    def handle(self, *args, **options):
        # 检查是否已存在admin用户
        if not User.objects.filter(username='links').exists():
            with transaction.atomic():
                user = User.objects.create_superuser(
                    username='links',
                    email='baiyila2022@gmail.com',
                    password='Baiyila7788.'
                )
                # 确保UserProfile被正确创建
                from authentication.models import UserProfile
                profile, created = UserProfile.objects.get_or_create(user=user)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS('Successfully created admin user "links" with profile')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS('Successfully created admin user "links"')
                    )
        else:
            # 如果用户存在，确保密码是正确的
            user = User.objects.get(username='links')
            user.set_password("Baiyila7788.")
            user.is_superuser = True
            user.is_staff = True
            user.save()
            # 确保UserProfile存在
            from authentication.models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Successfully updated admin user "links" and created profile')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Successfully updated admin user "links"')
                )