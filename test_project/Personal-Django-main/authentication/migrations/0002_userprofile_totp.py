# Generated for Google Authenticator (TOTP) 2FA

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='totp_secret',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='totp_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
