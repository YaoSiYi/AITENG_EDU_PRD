# Generated for TestCase updater (last modifier)

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('testcases', '0003_testcase_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='updater',
            field=models.ForeignKey(
                verbose_name='修改人',
                to=settings.AUTH_USER_MODEL,
                null=True,
                blank=True,
                on_delete=models.SET_NULL,
                related_name='updated_test_cases',
            ),
        ),
    ]

