from django.contrib import admin
from .models import Userprofile,Students, Course, Grade
import re


# Register your models here.
class students_admin(admin.ModelAdmin):
    list_display = ['sno','sname']

admin.site.register(Userprofile)
admin.site.register(Students,students_admin)
admin.site.register(Course)
admin.site.register(Grade)

# class StudentsAdmin(admin.ModelAdmin):
#     def gender(self):
#         if self.sex is True:
#             return '男'
#         else:
#             return '女'
#
#     gender.short_description = "性别"
#     list_display = ['sno', 'sname', 'sclass', gender, 'sage', 'sdept']
#     search_fields = ['sname']
#     list_filter = ['sname']
#     list_per_page = 10
#
#
# admin.site.register(Students, StudentsAdmin)
#
#
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['cno', 'cname', 'dept', 'teacher']
#     search_fields = ['cname']
#     list_filter = ['cname']
#     list_per_page = 10
#
#
# admin.site.register(Course, CourseAdmin)
#
#
# class GradeAdmin(admin.ModelAdmin):
#     def s_num(self):
#         temp = str(self.sno)
#         return re.findall(r'[(](.*?)[)]', temp)
#
#     def c_num(self):
#         temp = str(self.cno)
#         return re.findall(r'[(](.*?)[)]', temp)
#
#     s_num.short_description = "学号"
#     c_num.short_description = "课程号"
#
#     list_display = [s_num, c_num, 'grade']
#     search_fields = ['sno']
#     list_filter = ['sno']
#     list_per_page = 10
#
#
# admin.site.register(Grade, GradeAdmin)


# class UsernameAdmin(admin.ModelAdmin):
#     list_display = ['username', 'password', 'identity']
#     search_fields = ['username']
#     list_filter = ['password']
#     list_per_page = 10
#
#
# admin.site.register(user,UsernameAdmin)