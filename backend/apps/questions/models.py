from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class QuestionCategory(models.Model):
    """题目分类"""
    name = models.CharField('分类名称', max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'question_categories'
        verbose_name = '题目分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Question(models.Model):
    """题库模型"""
    STAGE_CHOICES = [
        (1, '阶段1'),
        (2, '阶段2'),
        (3, '阶段3'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    ]

    stage = models.IntegerField('阶段', choices=STAGE_CHOICES)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    subject = models.CharField('科目', max_length=50)
    difficulty = models.CharField('难度', max_length=20, choices=DIFFICULTY_CHOICES)
    content = models.TextField('题目内容')
    image = models.ImageField('题目图片', upload_to='questions/images/', null=True, blank=True)
    voice = models.FileField('题目语音', upload_to='questions/audio/', null=True, blank=True)
    answer = models.TextField('答案')
    explanation = models.TextField('解析', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'questions'
        verbose_name = '题目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.content[:30]}"


class WrongQuestion(models.Model):
    """错题本模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='题目')
    user_answer = models.TextField('用户答案', blank=True)
    is_correct = models.BooleanField('是否答对', default=False)
    attempt_count = models.IntegerField('尝试次数', default=1)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'wrong_questions'
        verbose_name = '错题'
        verbose_name_plural = '错题本'
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_user_question')
        ]

    def __str__(self):
        return f"{self.user.nickname} - {self.question.content[:20]}"


class Assignment(models.Model):
    """作业模型"""
    title = models.CharField('作业标题', max_length=200)
    stage = models.IntegerField('阶段', choices=Question.STAGE_CHOICES)
    question_count = models.IntegerField('题目数量', default=10)
    questions = models.ManyToManyField(Question, verbose_name='题目列表')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'assignments'
        verbose_name = '作业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UserAssignment(models.Model):
    """用户作业记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='作业')
    score = models.FloatField('得分', null=True, blank=True)
    completed = models.BooleanField('是否完成', default=False)
    started_at = models.DateTimeField('开始时间', auto_now_add=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)

    class Meta:
        db_table = 'user_assignments'
        verbose_name = '用户作业'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'assignment'], name='unique_user_assignment')
        ]

    def __str__(self):
        return f"{self.user.nickname} - {self.assignment.title}"
