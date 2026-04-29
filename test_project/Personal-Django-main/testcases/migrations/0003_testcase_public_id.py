# Generated for TestCase public_id (snowflake)

from django.db import migrations, models
import common.snowflake


def populate_public_id(apps, schema_editor):
    """
    为已有 TestCase 数据填充唯一的 snowflake public_id。
    单独在 Python 中逐条生成，避免 SQLite 在迁移时对 default 只评估一次导致唯一约束冲突。
    """
    TestCase = apps.get_model('testcases', 'TestCase')
    for obj in TestCase.objects.all():
        if not obj.public_id:
            obj.public_id = common.snowflake.generate_snowflake_id()
            obj.save(update_fields=['public_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('testcases', '0002_testcase_actual_result_testcase_case_type_and_more'),
    ]

    operations = [
        # 第一步：先加一个可为空、非唯一的字段，避免 SQLite 复制表时 unique+default 冲突
        migrations.AddField(
            model_name='testcase',
            name='public_id',
            field=models.BigIntegerField(
                verbose_name='公共ID',
                null=True,
                blank=True,
                default=None,
                editable=False,
            ),
        ),
        # 第二步：用 Python 填充已有行的唯一 ID
        migrations.RunPython(populate_public_id, migrations.RunPython.noop),
        # 第三步：再收紧为 unique + 默认使用 generate_snowflake_id
        migrations.AlterField(
            model_name='testcase',
            name='public_id',
            field=models.BigIntegerField(
                verbose_name='公共ID',
                unique=True,
                default=common.snowflake.generate_snowflake_id,
                editable=False,
            ),
        ),
    ]

