from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from django.contrib.auth.models import User

# Create your models here.

course_choices = (
    ('LinuxL1', u'Linux中高级'),
    ('LinuxL2', u'Linux架构师'),
    ('LinuxL151', u'Linux中高级(51网络)'),
    ('LinuxL251', u'Linux中高级+架构合成班(51网络)'),
    ('PythonDevOps', u'Python自动化开发'),
    ('PythonFullStack', u'Python高级全栈开发'),
    ('PythonDevOps51', u'Python自动化开发(51网络)'),
    ('PythonFullStack51', u'Python高级全栈开发(51网络)'),
    ('BigDataDev', u'大数据开发课程'),
    ('Cloud', u'云计算课程'),
)

class_type_choices = (
    ('online', u'网络班'),
    ('offline_weekend', u'面授班(周末)'),
    ('offline_fulltime', u'面授班(脱产)'),
)


@python_2_unicode_compatible
class UserProfile(models.Model):  # 用户配置表
    user = models.OneToOneField(User, verbose_name=u'用户名')
    name = models.CharField(max_length=32, verbose_name=u'姓名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'


@python_2_unicode_compatible
class School(models.Model):  # 学校表
    name = models.CharField(max_length=64, unique=True, verbose_name=u'校区名称')
    addr = models.CharField(max_length=128, verbose_name=u'地址')
    staffs = models.ManyToManyField('UserProfile', blank=True, verbose_name=u'员工')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'学校'
        verbose_name_plural = u'学校'


@python_2_unicode_compatible
class Course(models.Model):  # 课程表
    name = models.CharField(max_length=128, unique=True, verbose_name=u'课程名称', choices=course_choices)
    price = models.IntegerField(verbose_name=u'面授价格')
    online_price = models.IntegerField(verbose_name=u'网络班价格')
    brief = models.TextField(verbose_name=u'课程简介')

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = u'课程'


@python_2_unicode_compatible
class ClassList(models.Model):  # 班级表
    course = models.ForeignKey('Course', verbose_name=u'课程')
    course_type = models.CharField(choices=class_type_choices, max_length=32, verbose_name=u'课程类型')
    semester = models.IntegerField(verbose_name=u'学期')
    start_date = models.DateField(verbose_name=u'开班日期')
    graduate_date = models.DateField(blank=True, null=True, verbose_name=u'结业日期')
    teachers = models.ManyToManyField('UserProfile', verbose_name=u'讲师')

    def __str__(self):
        return "%s %s(%s)" % (self.course.get_name_display(), self.get_course_type_display(), self.semester)

    class Meta:
        verbose_name = u'班级列表'
        verbose_name_plural = u'班级列表'
        unique_together = ('course', 'course_type', 'semester')


@python_2_unicode_compatible
class Customer(models.Model):  # 客户表
    qq = models.CharField(max_length=64, unique=True, verbose_name=u'QQ号')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'姓名')
    phone = models.BigIntegerField(verbose_name=u'手机号', blank=True, null=True)
    stu_id = models.CharField(verbose_name=u'学号', blank=True, null=True, max_length=64)

    source_type = (
        ('qq', u'qq群'),
        ('referral', u'内部转介绍'),
        ('51cto', u'52cto'),
        ('agent', u'招生代理'),
        ('others', u'其它'),
    )

    source = models.CharField(verbose_name=u'客户来源', max_length=64, choices=source_type, default='qq')
    referral_from = models.ForeignKey('self',
                                      related_name='internal_referral',
                                      blank=True,
                                      null=True,
                                      verbose_name=u'转介绍学员',
                                      help_text=u'若此客户是转介绍内部学员,请在此处选择内部学员姓名')
    course = models.ForeignKey('Course', verbose_name=u'咨询课程')
    class_type = models.CharField(verbose_name=u'班级类型', max_length=64, choices=class_type_choices)
    customer_note = models.TextField(verbose_name=u'客户咨询内容详情', help_text=u'客户咨询的大概情况,客户个人信息备注等...')
    status_choices = (
        ('signed', u'已报名'),
        ('unregistered', u'未报名'),
        ('graduated', u'已毕业'),
    )
    status = models.CharField(verbose_name=u'状态', choices=status_choices, max_length=64, default='unregistered',
                              help_text=u'选择客户此时的状态')
    consultant = models.ForeignKey('UserProfile', verbose_name=u'课程顾问')
    date = models.DateField(verbose_name=u'咨询日期', auto_now_add=True)
    class_list = models.ManyToManyField('ClassList', verbose_name=u'已报班级', blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = u'客户'
        verbose_name_plural = u'客户'


@python_2_unicode_compatible
class ConsultRecord(models.Model):  # 咨询记录表
    customer = models.ForeignKey('Customer', verbose_name=u'所咨询的客户')
    note = models.TextField(verbose_name=u'跟进内容...')
    status_choices = (
        (1, u'近期无报名计划'),
        (2, u'2个月内报名'),
        (3, u'1个月内报名'),
        (4, u'2周内报名'),
        (5, u'1周内报名'),
        (6, u'2天内报名'),
        (7, u'已报名'),
    )
    status = models.IntegerField(verbose_name=u'状态', choices=status_choices, help_text=u'选择客户此时的状态')
    consultant = models.ForeignKey('UserProfile', verbose_name=u'跟进人')
    date = models.DateField(verbose_name=u'跟进日期', auto_now_add=True)

    def __str__(self):
        return u"%s, %s" % (self.customer, self.get_status_display())

    class Meta:
        verbose_name = u'客户咨询跟进记录'
        verbose_name_plural = u'客户咨询跟进记录'


@python_2_unicode_compatible
class CourseRecord(models.Model):  # 课程记录表
    course = models.ForeignKey('ClassList', verbose_name=u'班级(课程)')
    day_num = models.IntegerField(verbose_name=u'节次', help_text=u'此处填写第几节课或第几天课程...,必须为数字')
    date = models.DateField(auto_now_add=True, verbose_name=u'上课日期')
    teacher = models.ForeignKey('UserProfile', verbose_name=u'讲师')

    def __str__(self):
        return u'%s 第%s天' % (self.course, self.day_num)

    class Meta:
        verbose_name = u'上课记录'
        verbose_name_plural = u'上课记录'
        unique_together = ('course', 'day_num')


@python_2_unicode_compatible
class StudyRecord(models.Model):  # 学习记录表
    course_record = models.ForeignKey('CourseRecord', verbose_name=u'第几天课程')
    student = models.ForeignKey('Customer', verbose_name=u'姓名')
    record_choices = (
        ('checked', u'已签到'),
        ('late', u'迟到'),
        ('noshow', u'缺勤'),
        ('leave_early', u'早退'),
    )
    record = models.CharField(verbose_name=u'上课记录', choices=record_choices, max_length=64, default='checked')
    score_choices = (
        (1000, 'A++'),
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (70, 'B-'),
        (60, 'C+'),
        (50, 'C'),
        (40, 'C-'),
        (0, 'D'),
        (-1, 'N/A'),
        (-100, 'COPY'),
        (-1000, 'FAIL'),
    )

    score_color_select = {
        1000: "#5DFC70",
        100: "#5DFC70",
        90: "yellowgreen",
        85: "deepskyblue",
        80: "#49E3F5",
        70: "#1CD4C8",
        60: "#FFBF00",
        50: "#FF8000",
        40: "#FE642E",
        0: "red",
        -1: "#E9E9E9",
        -100: "#585858",
        -1000: "darkred",
    }

    record_color_select = {
        'checked': "#5DFC70",
        'late': "#FFBF00",
        'noshow': "#B40404",
        'leave_early': "#FFFF00",
    }
    score = models.IntegerField(verbose_name=u'本节成绩', choices=score_choices, default=-1)
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'日期')
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'备注')

    def __str__(self):
        return u"%s,学员:%s,记录:%s,成绩:%s,备注:%s" % (
            self.course_record, self.student.name, self.get_record_display(), self.get_score_display(), self.note)

    def record_color(self):
        html_st = format_html('<span style="padding:5px;background-color:%s;">%s</span>' % (
            self.record_color_select[self.record], self.get_record_display()
        ))
        return html_st

    def score_color(self):
        html_st = format_html('<span style="padding:5px;background-color:%s;">%s</span>' % (
            self.score_color_select[self.score], self.score
        ))
        return html_st

    record_color.short_description = u'签到情况'
    score_color.short_description = u'成绩'

    class Meta:
        verbose_name = u'学员学习记录'
        verbose_name_plural = u'学员学习记录'
        unique_together = ('course_record', 'student')
