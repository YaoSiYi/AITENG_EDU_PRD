from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import UserProfile

class Command(BaseCommand):
    help = 'Delete a user safely'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to delete')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            user_id = user.id
            
            # 删除相关的authtoken（如果有）
            try:
                from rest_framework.authtoken.models import Token
                Token.objects.filter(user=user).delete()
            except ImportError:
                pass
            
            # 删除用户资料
            try:
                user.profile.delete()
            except:
                pass
                
            # Delete the user
            user.delete()
            
            # Clean up any orphaned profiles
            UserProfile.objects.filter(user_id=user_id).delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted user "{username}"')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error deleting user "{username}": {str(e)}')
            )