from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class StudentStats(models.Model):
    """学员统计"""
    period = models.CharField('期数', max_length=50)
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50)
    count = models.IntegerField('人数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'student_stats'
        verbose_name = '学员统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.period} - {self.province} {self.city}: {self.count}人"


class Dormitory(models.Model):
    """宿舍管理"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='学员',
        related_name='dormitory_info',
        help_text='关联的学员用户，姓名、性别、期数、籍贯、手机号将自动从用户信息中获取'
    )
    student_name = models.CharField('姓名', max_length=50, help_text='学员姓名（自动从关联用户获取）')
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, blank=True, default='')
    period = models.CharField('期数', max_length=50, blank=True, default='')
    hometown = models.CharField('籍贯', max_length=100, blank=True, default='')
    dormitory = models.CharField('宿舍', max_length=50, help_text='宿舍号，例如：A栋101')
    phone = models.CharField('手机号', max_length=11, blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'dormitories'
        verbose_name = '宿舍管理'
        verbose_name_plural = verbose_name
        ordering = ['dormitory', 'student_name']

    def save(self, *args, **kwargs):
        """保存时自动从关联用户同步数据"""
        if self.student:
            # 从关联的用户中获取信息
            self.student_name = self.student.nickname or self.student.username
            if self.student.gender:
                self.gender = self.student.gender
            if self.student.period:
                self.period = self.student.period
            if self.student.hometown:
                self.hometown = self.student.hometown
            if self.student.phone:
                self.phone = self.student.phone
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dormitory} - {self.student_name}"


class EmploymentStats(models.Model):
    """就业统计"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='学员',
        related_name='employment_records',
        help_text='关联的学员用户，期数和性别将自动从用户信息中获取'
    )
    student_name = models.CharField('学员姓名', max_length=50, help_text='学员姓名（如果未关联用户则手动填写）')
    period = models.CharField('期数', max_length=50, default='', blank=True, help_text='学员期数（优先从关联用户获取）')
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, blank=True, default='', help_text='学员性别（优先从关联用户获取）')
    city = models.CharField('城市', max_length=50)
    company = models.CharField('公司', max_length=200)
    position = models.CharField('职位', max_length=100)
    salary = models.IntegerField('薪资')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'employment_stats'
        verbose_name = '就业统计'
        verbose_name_plural = verbose_name
        ordering = ['-salary']

    def save(self, *args, **kwargs):
        """保存时自动从关联用户同步期数和性别"""
        if self.student:
            # 从关联的用户中获取期数和性别
            if self.student.period:
                self.period = self.student.period
            if self.student.gender:
                self.gender = self.student.gender
            # 如果学员姓名为空，使用用户的昵称或用户名
            if not self.student_name:
                self.student_name = self.student.nickname or self.student.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} - {self.company} - {self.salary}"


class ExcellentStudent(models.Model):
    """优秀学员"""
    name = models.CharField('姓名', max_length=50)
    avatar = models.ImageField('头像', upload_to='students/')
    period = models.CharField('期数', max_length=50)
    company = models.CharField('就业公司', max_length=200)
    position = models.CharField('职位', max_length=100)
    salary = models.IntegerField('薪资')
    testimonial = models.TextField('感言', blank=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'excellent_students'
        verbose_name = '优秀学员'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.company}"


class InterviewQuestion(models.Model):
    """高频面试题"""
    question = models.TextField('问题')
    answer = models.TextField('答案')
    category = models.CharField('分类', max_length=50)
    frequency = models.IntegerField('出现频率', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'interview_questions'
        verbose_name = '面试题'
        verbose_name_plural = verbose_name
        ordering = ['-frequency']

    def __str__(self):
        return self.question[:50]
