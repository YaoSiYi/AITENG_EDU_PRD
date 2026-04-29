"""
项目内「公共 ID」约定：对外主 ID 统一使用雪花算法（common.snowflake.generate_snowflake_id）。

- 新模型需要对外暴露主 id 时：增加 public_id 字段（BigIntegerField, unique, default=generate_snowflake_id）。
- API 层：列表/详情的响应中 id 使用 public_id（可返回为字符串避免前端大数精度问题）；
  URL 中的资源标识使用 public_id，例如 GET/PATCH/DELETE /api/resource/<public_id>/。
- 导出/勾选等参数中的 ids 传 public_id（逗号分隔）。

已有实现：testcases.TestCase 已按上述方式使用 public_id。
"""
from django.db import models
from common.snowflake import generate_snowflake_id


class SnowflakeIdMixin(models.Model):
    """
    混入后模型拥有 public_id 字段（雪花算法），可作为对外主 ID 使用。
    子类需在 Meta 中设置 abstract = True，或本类设为 abstract。
    """
    public_id = models.BigIntegerField(
        '公共ID',
        unique=True,
        default=generate_snowflake_id,
        editable=False,
    )

    class Meta:
        abstract = True
