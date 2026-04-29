We need to apply the suggested edit to the original code. The original code imports and prints from three models. The suggested edit changes the import style, modifies the output for StudentStats, adds new print sections for ES statistics, and does not include ExcellentStudent printing. The instruction is to output the complete modified file after applying the suggested edit. The suggested edit includes changes to the first part: changing path, setting environment variable differently, importing EmploymentStats as ES, and then removing the original prints and adding new prints. It also omits the ExcellentStudent loop. So we need to produce the code exactly as in the suggested edit, but we must preserve unchanged code exactly as-is? The instruction says "Leave existing comments in place unless changes require modifying them. Preserve all unchanged code exactly as-is." However, the suggested edit is a complete replacement of the original code's logic, so we have to apply the suggested edit. The original code's comments are mostly preserved except where changed. The suggested edit does not include the line `from apps.stats.models import EmploymentStats, ExcellentStudent, StudentStats` but imports ES, ExcellentStudent, StudentStats. Also the original print for EmploymentStats is replaced with new prints. The ExcellentStudent loop is removed entirely. So the final code should be exactly the suggested edit. But note: the original code had a docstring? No. The suggested edit starts with `import os, sys` and ends with the last print. So we output that block.

Also note: the suggested edit adds `from django.db.models import Count, Avg`. That's an addition. Also the environment variable setting uses `os.environ['DJANGO_SETTINGS_MODULE']` without setdefault. We'll output as given.

Thus final answer is the code block in the suggested edit.```python
import os, sys
sys.path.insert(0, os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from apps.stats.models import EmploymentStats as ES, ExcellentStudent, StudentStats
from django.db.models import Count, Avg

print('=== StudentStats (学员统计 - 就业率计算来源) ===')
for e in StudentStats.objects.all().order_by('id'):
    print(f'  ID:{e.id} period:{e.period} 总学员:{e.total_students} 就业:{e.employed_students} 未就业:{e.unemployed_students} 就业率:{e.employment_rate}% 最高薪资:{e.max_salary} 平均薪资:{e.avg_salary}')
print()
print('=== ES 按学期统计 ===')
for p in ES.objects.values('period').annotate(cnt=Count('id'), avg_s=Avg('salary')).order_by('period'):
    print(f'  period:{p["period"]} 人数:{p["cnt"]} 平均薪资:{p["avg_s"]:.0f}')
print()
print('=== 汇总 ===')
total = ES.objects.count()
avg = ES.objects.aggregate(Avg('salary'))
print(f'  总就业人数: {total}, 平均薪资: {avg["salary__avg"]:.0f}')

print()
print('=== 检查脏数据: created_at 异常 ===')
for e in ES.objects.all().order_by('created_at'):
    print(f'  ID:{e.id} created:{e.created_at} period:{e.period}')

