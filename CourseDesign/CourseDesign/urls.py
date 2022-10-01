"""CourseDesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Content.views import *
# admin123
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',UserViews.as_view()),
    path('get_token/',LoginViews.as_view()),
    path('log_out/',LogoutView.as_view()),
    path('init/',InitialView.as_view()),
    path('StudentGrade/',StudentGrade.as_view()),
    path('StudentChooseClass/',StudentChooseClassView.as_view()),
    path('StudentChooseClassUtility/',StudentChooseClass.as_view()),
    path('CreateClass/',TeacherCreateCourse.as_view()),
    path('SearchClass/',SearchClass.as_view()),
    path('TeacherSearchGrade/',TeacherSearchGrade.as_view()),
    path('SearchDept/',SearchDept.as_view()),
    path('SearchStudent/',SearchStudent.as_view()),
    path('UpdateStudentInfo/',UpdateStudentInfo.as_view()),
    path('SearchCourseDept/',SearchCourseDept.as_view()),
    path('SearchCourse/',SearchCourse.as_view()),
    path('UpdateCourseInfo/',UpdateCourseInfo.as_view()),
    path('GetGradeInfo/',GetGradeInfo.as_view()),
    path('SearchGrade/',SearchGrade.as_view()),
    path('UpdateGradeInfo/',UpdateGradeInfo.as_view()),
    path('SearchStudentClass/',SearchStudentClass.as_view()),
    path('SearchCourseDept/',SearchCourseDept.as_view()),
    path('AdminChooseClassView/',AdminChooseClassView.as_view()),
    path('GetAllData/',GetAllData.as_view()),
]
