from django.db import models


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=50, verbose_name='认证Token', default=1)
    phone = models.CharField(max_length=20)
    identity = models.IntegerField(choices=((0, '学生'), (1, '老师'), (2, '管理员')), )


class Students(models.Model):
    sno = models.CharField("学号", max_length=10,primary_key=True)
    sname = models.CharField("姓名", max_length=20,null=True)
    sclass = models.CharField("班级", max_length=20,null=True)
    sex = models.BooleanField("性别", default=True)
    sage = models.IntegerField("年龄",default=0)
    sdept = models.CharField("院系", max_length=100,null=True)


class Course(models.Model):
    cno = models.CharField("课程号", max_length=10,primary_key=True)
    cname = models.CharField("课程名", max_length=100,null=True)
    dept = models.CharField("开课院系", max_length=100,null=True)
    teacher = models.CharField("开课老师", max_length=20,null=True)


class Grade(models.Model):
    sno = models.ForeignKey('Students',on_delete=models.CASCADE)
    cno = models.ForeignKey('Course',on_delete=models.CASCADE)
    grade = models.IntegerField("成绩", null=True)
