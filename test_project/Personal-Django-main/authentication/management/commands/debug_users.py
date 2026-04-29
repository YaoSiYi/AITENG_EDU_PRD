from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import UserProfile
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug user and profile issues'

    def handle(self, *args, **options):
        self.stdout.write("Checking users and profiles...")
        
        # Check all users
        users = User.objects.all()
        self.stdout.write(f"Total users: {users.count()}")
        
        for user in users:
            self.stdout.write(f"User: {user.username} (ID: {user.id})")
            self.stdout.write(f"  - Email: {user.email}")
            self.stdout.write(f"  - Is staff: {user.is_staff}")
            self.stdout.write(f"  - Is superuser: {user.is_superuser}")
            
            # Check if user has profile
            try:
                profile = user.profile
                self.stdout.write(f"  - Profile ID: {profile.id}")
                self.stdout.write(f"  - Public ID: {profile.public_id}")
            except UserProfile.DoesNotExist:
                self.stdout.write("  - NO PROFILE FOUND")
            except Exception as e:
                self.stdout.write(f"  - PROFILE ERROR: {str(e)}")
                
        # Check for orphaned profiles
        profiles = UserProfile.objects.select_related('user').all()
        self.stdout.write(f"\nTotal profiles: {profiles.count()}")
        
        for profile in profiles:
            try:
                user = profile.user
                self.stdout.write(f"Profile {profile.id} linked to user {user.username}")
            except User.DoesNotExist:
                self.stdout.write(f"Orphaned profile: {profile.id}")
            except Exception as e:
                self.stdout.write(f"Profile {profile.id} error: {str(e)}")
                
        self.stdout.write("Debug completed.")