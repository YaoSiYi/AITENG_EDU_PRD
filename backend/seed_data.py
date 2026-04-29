#!/usr/bin/env python
"""
初始数据脚本 - 为艾腾教育系统添加测试数据
"""
import os, sys, django
sys.path.insert(0, '/Users/yao/Node_Project/Aiteng_Edu_Prd/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.questions.models import Question, QuestionCategory
from apps.activities.models import Activity
from apps.stats.models import EmploymentStats, ExcellentStudent, InterviewQuestion, StudentStats
from apps.evaluations.models import Evaluation, StudentProgress

def create_users():
    print("\n=== 创建用户 ===")
    users_data = [
        dict(username='teacher01', email='teacher01@aiteng.com', password='aiteng123',
             nickname='王老师', hometown='上海', role='teacher'),
        dict(username='teacher02', email='teacher02@aiteng.com', password='aiteng123',
             nickname='李老师', hometown='北京', role='teacher'),
        dict(username='student01', email='student01@aiteng.com', password='aiteng123',
             nickname='张同学', hometown='广州', role='student'),
        dict(username='student02', email='student02@aiteng.com', password='aiteng123',
             nickname='刘同学', hometown='深圳', role='student'),
        dict(username='student03', email='student03@aiteng.com', password='aiteng123',
             nickname='陈同学', hometown='成都', role='student'),
        dict(username='student04', email='student04@aiteng.com', password='aiteng123',
             nickname='赵同学', hometown='武汉', role='student'),
    ]
    created = []
    for d in users_data:
        if not User.objects.filter(username=d['username']).exists():
            u = User.objects.create_user(**d)
            created.append(u)
            print(f"  ✅ {d['nickname']} ({d['role']})")
        else:
            u = User.objects.get(username=d['username'])
            created.append(u)
            print(f"  ⏭  {d['nickname']} 已存在")
    return created

def create_categories():
    print("\n=== 创建题目分类 ===")
    categories_data = [
        '软件测试基础', '功能与非功能测试', 'Linux和MySQL', 'Python课程',
        'UI自动化', '接口测试', '性能测试', '接口自动化', '项目实战', 'AI大模型与Agent'
    ]
    created = []
    for name in categories_data:
        cat, is_new = QuestionCategory.objects.get_or_create(name=name)
        created.append(cat)
        print(f"  {'✅' if is_new else '⏭ '} {name}")
    return created

def create_questions(categories):
    print("\n=== 创建题目 ===")
    questions_data = [
        dict(stage=1, category=categories[0], subject='软件测试基础', difficulty='easy',
             content='软件测试生命周期（STLC）包含哪些主要阶段？\nA. 需求分析、测试计划、测试设计、测试执行、缺陷跟踪、测试报告\nB. 需求分析、编码、测试、发布\nC. 计划、设计、开发、测试\nD. 以上都不对',
             answer='A', explanation='软件测试生命周期包含需求分析、测试计划、测试设计、测试环境搭建、测试执行、缺陷跟踪、测试报告、测试总结8个主要阶段。'),
        dict(stage=1, category=categories[0], subject='软件测试基础', difficulty='medium',
             content='黑盒测试和白盒测试的主要区别是什么？\nA. 黑盒测试关注内部结构，白盒测试关注外部功能\nB. 黑盒测试关注外部功能，白盒测试关注内部结构\nC. 两者没有区别\nD. 黑盒测试更难',
             answer='B', explanation='黑盒测试是从用户角度测试软件功能，不关心内部实现；白盒测试是从开发角度测试代码逻辑和结构。'),
        dict(stage=2, category=categories[1], subject='功能测试', difficulty='medium',
             content='等价类划分法的主要目的是什么？\nA. 增加测试用例数量\nB. 减少测试用例数量同时保证覆盖率\nC. 提高测试速度\nD. 降低测试成本',
             answer='B', explanation='等价类划分法通过将输入域划分为若干等价类，从每个等价类中选取代表性数据进行测试，既保证了测试覆盖率，又减少了测试用例数量。'),
        dict(stage=3, category=categories[2], subject='Linux基础', difficulty='easy',
             content='在Linux中，查看当前目录下所有文件（包括隐藏文件）的命令是？\nA. ls\nB. ls -l\nC. ls -a\nD. ls -h',
             answer='C', explanation='ls -a 命令可以显示所有文件，包括以.开头的隐藏文件。'),
        dict(stage=3, category=categories[2], subject='MySQL基础', difficulty='medium',
             content='MySQL中，哪个关键字用于去除查询结果中的重复行？\nA. UNIQUE\nB. DISTINCT\nC. DIFFERENT\nD. REMOVE',
             answer='B', explanation='DISTINCT关键字用于返回唯一不同的值，去除重复行。'),
        dict(stage=1, category=categories[3], subject='Python基础', difficulty='easy',
             content='Python中，哪个数据类型是可变的？\nA. tuple\nB. str\nC. list\nD. int',
             answer='C', explanation='list是可变数据类型，可以修改其元素；而tuple、str、int都是不可变类型。'),
        dict(stage=2, category=categories[4], subject='Selenium基础', difficulty='medium',
             content='Selenium中，定位元素的8种方法不包括以下哪一种？\nA. id\nB. name\nC. class_name\nD. color',
             answer='D', explanation='Selenium的8种定位方法是：id、name、class_name、tag_name、link_text、partial_link_text、xpath、css_selector。'),
        dict(stage=2, category=categories[5], subject='接口测试', difficulty='medium',
             content='HTTP状态码200表示什么？\nA. 请求失败\nB. 请求成功\nC. 重定向\nD. 服务器错误',
             answer='B', explanation='HTTP状态码200表示请求成功，服务器已成功处理了请求。'),
        dict(stage=3, category=categories[6], subject='性能测试', difficulty='hard',
             content='在性能测试中，TPS是什么意思？\nA. 每秒事务数\nB. 总处理时间\nC. 测试通过率\nD. 线程池大小',
             answer='A', explanation='TPS（Transactions Per Second）表示每秒事务数，是衡量系统性能的重要指标。'),
        dict(stage=3, category=categories[7], subject='接口自动化', difficulty='hard',
             content='Pytest框架中，哪个装饰器用于参数化测试？\nA. @pytest.fixture\nB. @pytest.mark.parametrize\nC. @pytest.setup\nD. @pytest.param',
             answer='B', explanation='@pytest.mark.parametrize装饰器用于参数化测试，可以用不同的参数多次运行同一个测试函数。'),
    ]

    created = 0
    for data in questions_data:
        if not Question.objects.filter(content=data['content']).exists():
            Question.objects.create(**data)
            created += 1
            print(f"  ✅ {data['subject']} - {data['difficulty']}")
        else:
            print(f"  ⏭  {data['subject']} 已存在")

    print(f"\n  共创建 {created} 道题目")
    return created

def create_activities(users):
    print("\n=== 创建活动 ===")
    admin = User.objects.get(username='admin')
    activities_data = [
        dict(creator=admin, title='Python编程挑战赛',
             description='完成50道Python编程题，掌握Python核心语法和数据处理能力。活动时间：2024年4月15日-4月30日',
             is_active=True),
        dict(creator=admin, title='UI自动化实战周',
             description='连续7天完成Selenium自动化测试实战，养成自动化测试习惯。每天一个实战项目，从基础到进阶。',
             is_active=True),
        dict(creator=admin, title='接口测试马拉松',
             description='参与接口测试实战，掌握Postman和接口自动化测试技能。包含RESTful API测试、接口文档编写等内容。',
             is_active=True),
        dict(creator=admin, title='性能测试训练营',
             description='学习JMeter性能测试工具，掌握性能测试方法论。包含压力测试、负载测试、稳定性测试等。',
             is_active=True),
        dict(creator=admin, title='金融项目实战',
             description='完成金融项目的完整测试流程，从需求分析到测试报告。真实项目场景，提升实战能力。',
             is_active=False),
    ]

    created = 0
    for data in activities_data:
        if not Activity.objects.filter(title=data['title']).exists():
            Activity.objects.create(**data)
            created += 1
            print(f"  ✅ {data['title']}")
        else:
            print(f"  ⏭  {data['title']} 已存在")

    print(f"\n  共创建 {created} 个活动")
    return created

def create_employment_stats():
    print("\n=== 创建就业统计 ===")
    stats_data = [
        dict(student_name='张伟', company='阿里巴巴', position='高级测试工程师', salary=28000, city='杭州'),
        dict(student_name='李娜', company='腾讯', position='测试开发工程师', salary=32000, city='深圳'),
        dict(student_name='王强', company='字节跳动', position='测试工程师', salary=26000, city='北京'),
        dict(student_name='刘芳', company='美团', position='高级测试工程师', salary=25000, city='北京'),
        dict(student_name='陈明', company='百度', position='测试工程师', salary=22000, city='北京'),
        dict(student_name='赵丽', company='京东', position='测试开发工程师', salary=24000, city='北京'),
        dict(student_name='孙杰', company='网易', position='高级测试工程师', salary=23000, city='杭州'),
        dict(student_name='周敏', company='滴滴', position='测试工程师', salary=21000, city='北京'),
    ]

    created = 0
    for data in stats_data:
        if not EmploymentStats.objects.filter(student_name=data['student_name']).exists():
            EmploymentStats.objects.create(**data)
            created += 1
            print(f"  ✅ {data['student_name']} - {data['company']} - {data['salary']}元")
        else:
            print(f"  ⏭  {data['student_name']} 已存在")

    print(f"\n  共创建 {created} 条就业记录")
    return created

def create_excellent_students():
    print("\n=== 创建优秀学员 ===")
    students_data = [
        dict(name='张伟', period='2024年1期', company='阿里巴巴', salary=28000,
             testimonial='艾腾教育的课程体系非常完善，从基础到进阶都有详细的讲解。老师们经验丰富，实战项目让我快速成长。',
             is_featured=True),
        dict(name='李娜', period='2024年1期', company='腾讯', salary=32000,
             testimonial='通过艾腾教育的学习，我从零基础到成功入职腾讯。课程内容实用，项目经验丰富，非常感谢老师们的指导。',
             is_featured=True),
        dict(name='王强', period='2023年12期', company='字节跳动', salary=26000,
             testimonial='艾腾教育的AI大模型测试课程让我在面试中脱颖而出，成功拿到字节跳动的offer。',
             is_featured=True),
    ]

    created = 0
    for data in students_data:
        if not ExcellentStudent.objects.filter(name=data['name'], period=data['period']).exists():
            ExcellentStudent.objects.create(**data)
            created += 1
            print(f"  ✅ {data['name']} - {data['company']}")
        else:
            print(f"  ⏭  {data['name']} 已存在")

    print(f"\n  共创建 {created} 位优秀学员")
    return created

def create_interview_questions():
    print("\n=== 创建面试题 ===")
    questions_data = [
        dict(question='请描述软件测试的生命周期', category='基础理论', frequency=95,
             answer='软件测试生命周期包括：需求分析、测试计划、测试设计、测试环境搭建、测试执行、缺陷跟踪、测试报告、测试总结。'),
        dict(question='黑盒测试和白盒测试的区别', category='基础理论', frequency=92,
             answer='黑盒测试关注外部功能，不关心内部实现；白盒测试关注内部代码逻辑和结构。'),
        dict(question='如何设计测试用例', category='测试方法', frequency=88,
             answer='常用方法包括：等价类划分、边界值分析、判定表、因果图、正交试验法、场景法等。'),
        dict(question='Selenium如何处理弹窗', category='自动化测试', frequency=85,
             answer='使用switch_to.alert()方法切换到弹窗，然后使用accept()接受或dismiss()取消。'),
        dict(question='接口测试的重点是什么', category='接口测试', frequency=90,
             answer='重点包括：功能验证、参数校验、异常处理、性能测试、安全测试等。'),
        dict(question='性能测试的关键指标', category='性能测试', frequency=87,
             answer='关键指标包括：响应时间、吞吐量（TPS）、并发用户数、资源利用率、错误率等。'),
    ]

    created = 0
    for data in questions_data:
        if not InterviewQuestion.objects.filter(question=data['question']).exists():
            InterviewQuestion.objects.create(**data)
            created += 1
            print(f"  ✅ {data['question'][:30]}...")
        else:
            print(f"  ⏭  {data['question'][:30]}... 已存在")

    print(f"\n  共创建 {created} 道面试题")
    return created

def create_student_stats():
    print("\n=== 创建学员统计 ===")
    stats_data = [
        dict(period='2024-01', province='北京', city='北京市', count=156),
        dict(period='2024-01', province='上海', city='上海市', count=98),
        dict(period='2024-01', province='广东', city='深圳市', count=124),
        dict(period='2024-01', province='广东', city='广州市', count=87),
        dict(period='2024-01', province='浙江', city='杭州市', count=76),
        dict(period='2024-02', province='北京', city='北京市', count=168),
        dict(period='2024-02', province='上海', city='上海市', count=105),
        dict(period='2024-02', province='广东', city='深圳市', count=132),
    ]

    created = 0
    for data in stats_data:
        if not StudentStats.objects.filter(period=data['period'], city=data['city']).exists():
            StudentStats.objects.create(**data)
            created += 1
            print(f"  ✅ {data['period']} - {data['city']} - {data['count']}人")
        else:
            print(f"  ⏭  {data['period']} - {data['city']} 已存在")

    print(f"\n  共创建 {created} 条学员统计")
    return created

def main():
    print("=" * 60)
    print("艾腾教育 - 初始数据导入")
    print("=" * 60)

    users = create_users()
    categories = create_categories()
    questions_count = create_questions(categories)
    activities_count = create_activities(users)
    employment_count = create_employment_stats()
    excellent_count = create_excellent_students()
    interview_count = create_interview_questions()
    student_stats_count = create_student_stats()

    print("\n" + "=" * 60)
    print("数据导入完成！")
    print("=" * 60)
    print(f"✅ 用户: {len(users)} 个")
    print(f"✅ 题目分类: {len(categories)} 个")
    print(f"✅ 题目: {questions_count} 道")
    print(f"✅ 活动: {activities_count} 个")
    print(f"✅ 就业记录: {employment_count} 条")
    print(f"✅ 优秀学员: {excellent_count} 位")
    print(f"✅ 面试题: {interview_count} 道")
    print(f"✅ 学员统计: {student_stats_count} 条")
    print("\n🎉 所有初始数据已成功导入！")
    print("\n你现在可以访问以下地址查看数据：")
    print("  - 前端: http://localhost:3000")
    print("  - 后台: http://localhost:8000/admin")
    print("  - API文档: http://localhost:8000/api/docs")

if __name__ == '__main__':
    main()
