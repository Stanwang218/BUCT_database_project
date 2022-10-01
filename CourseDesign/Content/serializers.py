from rest_framework import serializers
from .models import Students, Course


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['sno', 'sname', 'sclass', 'sex', 'sage', 'sdept']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['cno', 'cname', 'dept', 'teacher']


# class gradeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = grade
#         fields = ['sno', 'cno', 'grade']
#
#
# class userSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = user
#         fields = ['username', 'password', 'identity']
