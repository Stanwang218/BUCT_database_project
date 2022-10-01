from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views import View
from django.contrib import auth
from django.utils.decorators import method_decorator
from .models import Userprofile, Students, Course, Grade
import hashlib
import json
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


class InitialView(View):
    def get(self, request):
        users = User.objects.all()
        student_list = []
        course_list = []
        for user in users:
            if user.userprofile.identity == 0:
                student_list.append({
                    'number': user.username,
                    'name': user.last_name + user.first_name
                })

        for list in student_list:
            student = Students(sno=list['number'], sname=list['name'])
            student.save()
        # for list in course_list:
        #     course = Course(teacher=list['name'])
        #     course.save()
        return HttpResponse("初始化成功")


class UserViews(View):
    def get(self, request):
        users = User.objects.all()
        print(users)
        res_list = []
        for user in users:
            res_list.append({
                'username': user.username,
                'phone': user.userprofile.phone
            }
            )
        # users = serializers.serialize("json",users)
        return JsonResponse(
            {
                'code': 0,
                'message': '查询成功',
                'contents': res_list
            }, json_dumps_params={"ensure_ascii": False})


# 登录接口
class LoginViews(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        username = payload.get('username')
        password = payload.get('password')
        ids = payload.get('identity')
        # print(username)
        # print(password)
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse({
                'message': 'fail',
            })
        else:
            token = self.generate_token(username)
            user.userprofile.token = token
            user.userprofile.save()
            user.save()
            if user.userprofile.identity != ids:
                return JsonResponse({
                    'message': 'fail',
                })
            else:
                auth.login(request, user)
                print(request.session.session_key)
                return JsonResponse(
                    {
                        'id': user.id,
                        'message': 'success',
                        'identity': user.userprofile.identity,
                        'name': user.last_name + user.first_name,
                        'token': token,
                        'username': user.username,
                    }, json_dumps_params={"ensure_ascii": False}
                )

    def generate_token(self, username):
        return hashlib.md5(username.encode("utf-8")).hexdigest()


# 退出接口
class LogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        user_id = payload.get('id')
        name = payload.get('name')
        token = payload.get('token')
        user = Userprofile.objects.filter(token=token).update(token=1)
        # print(user)
        return HttpResponse("退出成功")


# 学生成绩查询接口
class StudentGrade(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payloads = json.loads(request.body)
        # username 为学号
        student_name = payloads.get('username')
        cno = payloads.get('cno')
        if cno == '':
            grades = Grade.objects.filter(sno=student_name)
        else:
            grades = Grade.objects.filter(sno=student_name,cno=cno)
        cname_list = []
        grade_list = []
        dept_list = []
        teacher_list = []
        cno_list = []

        for grade in grades:
            if grade.grade is not None:
                temp = grade.cno
                cno_list.append(temp.cno)
                cname_list.append(grade.cno.cname)
                grade_list.append(grade.grade)
                teacher_list.append(grade.cno.teacher)
                dept_list.append(grade.cno.dept)
        return JsonResponse({
            'cno':cno_list,
            'cname': cname_list,
            'grade': grade_list,
            'dept': dept_list,
            'teacher': teacher_list,
        })


# 查询学生能选择课程的接口
class StudentChooseClassView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        username = payload.get('username')
        courses = Course.objects.all()
        # 获取所有科目

        grades = Grade.objects.filter(sno=username)
        # 获取我已经修完的课
        cno_finished_list = []
        cno_chosen_list = []
        for grade in grades:
            temp = grade.cno
            if grade.grade is not None:
                cno_finished_list.append(temp.cno)
            else:
                cno_chosen_list.append(temp.cno)
        # print(grades)

        cno_list = []
        cname_list = []
        dept_list = []
        teacher_list = []
        flag = []

        for course in courses:
            if course.cno not in cno_finished_list:
                cno_list.append(course.cno)
                cname_list.append(course.cname)
                teacher_list.append(course.teacher)
                dept_list.append(course.dept)
                if course.cno in cno_chosen_list:
                    flag.append(1)
                    # 已经选课
                else:
                    flag.append(0)
                    # 还未选课
        # print(cno_list)
        # print(cname_list)
        # print(teacher_list)
        # print(dept_list)
        return JsonResponse({
            'cno': cno_list,
            'cname': cname_list,
            'dept': dept_list,
            'teacher': teacher_list,
            'state': flag,
        })


# 查询学生所选择课程的接口
class StudentChooseClass(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        sno = payload.get('sno')
        cno = payload.get('cno')
        state = payload.get('state')
        # 退课
        if state == 1:
            grade = Grade.objects.get(sno=sno, cno=cno)
            if grade is None:
                return HttpResponse("无该实例")
            else:
                grade.delete()
                return HttpResponse("退课成功")

        # 选课
        else:
            student = Students.objects.get(sno=sno)
            course = Course.objects.get(cno=cno)
            if student is None or course is None:
                return HttpResponse("无该实例")
            else:
                grade = Grade(sno=student, cno=course, grade=None)
                grade.save()
                return HttpResponse("选课成功")


# 老师创建课程的接口
class TeacherCreateCourse(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        cno = payload.get('cno')
        cname = payload.get('cname')
        dept = payload.get('dept')
        name = payload.get('name')
        # print(cno)
        course = Course.objects.filter(cno=cno)
        # print(course)
        if not course.exists():
            course = Course(cno=cno, cname=cname, dept=dept, teacher=name)
            course.save()
            return HttpResponse("success")
        else:
            return HttpResponse("fail")


# 查询该老师开课情况接口
class SearchClass(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        name = payload.get('name')
        courses = Course.objects.filter(teacher=name)
        course_name = []
        # print(course_name)
        if not courses.exists():
            return JsonResponse({
                'courese': None
            })
        else:
            for course in courses:
                course_name.append(course.cname)
            return JsonResponse({
                'course': course_name
            })


# 老师查询对应的课程接口
class TeacherSearchGrade(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        cname = payload.get('cname')
        teacher = payload.get('teacher')
        sclass = payload.get('sclass')
        if cname == '全部':
            courses = Course.objects.filter(teacher=teacher)
            student_numbers = []
            course_numbers = []
            course_name = []
            # 老师所开课程
            for course in courses:
                # course_numbers.append(course.cno)
                course_number = course.cno
                grades = Grade.objects.filter(cno=course_number)
                # 每个课程检索成绩
                for grade in grades:
                    temp = grade.sno
                    cno = grade.cno
                    if sclass == '' or temp.sclass == sclass:
                        student_numbers.append(temp.sno)
                        course_numbers.append(cno.cno)
                        course_name.append(cno.cname)
            # 查询符合条件的选课的学生
            # print(student_numbers)
            # print(course_numbers)
            # print(course_name)
            # print(student_numbers)  #['2019040460']
            name_list = []
            class_list = []
            dept_list = []
            grade_list = []
            sname_list = []
            i = 0
            for student_number in student_numbers:
                course_number = course_numbers[i]
                student = Students.objects.get(sno=student_number)
                course = Course.objects.get(cno=course_number)
                grades = Grade.objects.filter(sno=student, cno=course)
                for grade in grades:
                    name_list.append(grade.sno.sname)
                    class_list.append(grade.sno.sclass)
                    dept_list.append(grade.sno.sdept)
                    if grade.grade is None:
                        grade_list.append('无')
            i = i + 1

            return JsonResponse({
                'cno':course_numbers,
                'sno':student_numbers,
                'name':name_list,
                'dept':dept_list,
                'grade':grade_list,
                'class':class_list,
                'cname':course_name
            })
        else:
            courses = Course.objects.filter(cname=cname)
            for course in courses:
                if course.teacher == teacher:
                    break
            cno = course.cno
            sno_list = []
            sname_list = []
            sclass_list = []
            sdept_list = []
            grade_list = []
            course_list = []
            grades = Grade.objects.filter(cno=cno)
            if grades is None:
                return HttpResponse('fail')
            for grade in grades:
                temp = grade.sno
                if sclass == '' or temp.sclass == sclass:
                    sno_list.append(temp.sno)
                    sname_list.append(grade.sno.sname)
                    sclass_list.append(grade.sno.sclass)
                    sdept_list.append(grade.sno.sdept)
                    course_list.append(cname)
                    if grade.grade is None:
                        grade_list.append('无')
                    else:
                        grade_list.append(grade.grade)
            # print(sclass_list)
            return JsonResponse({
                'sno': sno_list,
                'name': sname_list,
                'dept': sdept_list,
                'grade': grade_list,
                'class': sclass_list,
                'cname':course_list,
            })


# 查询已有学生的部门接口
class SearchDept(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        depts = Students.objects.values('sdept').distinct()
        dept_list = []
        for dept in depts:
            dept_list.append(dept['sdept'])
        print(dept_list)
        return JsonResponse({
            'dept':dept_list
        })


# 查询对应要求学生接口
class SearchStudent(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        payload = json.loads(request.body)
        sdept = payload.get('dept')
        sclass = payload.get('class')
        sex = payload.get('sex')
        # print(sdept)
        # print(sclass)
        # print(sex)
        sno_list = []
        name_list = []
        sex_list = []
        class_list = []
        dept_list = []
        print(sex)
        if sclass == '':
            if sdept == '全部':
                if sex == 2:
                    students = Students.objects.all()
                else:
                    students = Students.objects.filter(sex=sex)
            else:
                if sex == 2:
                    students = Students.objects.filter(sdept=sdept)
                else:
                    students = Students.objects.filter(sdept=sdept,sex=sex)
        else:
            if sdept == '全部':
                if sex == 2:
                    students = Students.objects.filter(sclass=sclass)
                else:
                    students = Students.objects.filter(sclass=sclass,sex=sex)
            else:
                if sex == 2:
                    students = Students.objects.filter(sclass=sclass,sdept=sdept)
                else:
                    students = Students.objects.filter(sclass=sclass,sdept=sdept, sex=sex)
        for student in students:
            sno_list.append(student.sno)
            name_list.append(student.sname)
            if student.sex is True:
                sex_list.append('男')
            else:
                sex_list.append('女')
            class_list.append(student.sclass)
            dept_list.append(student.sdept)
        print(class_list)
        return JsonResponse({
            'sno':sno_list,
            'sname':name_list,
            'sex':sex_list,
            'class':class_list,
            'dept':dept_list,
        })


# 更新学生信息接口
class UpdateStudentInfo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        sno = payload.get('sno')
        sname = payload.get('sname')
        sex = payload.get('sex')
        sclass = payload.get('sclass')
        dept = payload.get('dept')
        student = Students.objects.get(sno=sno)
        student.sname = sname
        student.sex = sex
        student.sclass = sclass
        student.sdept = dept
        student.save()
        print(student)
        return HttpResponse('更新成功')


# 查询已有课程的部门接口
class SearchCourseDept(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        depts = Course.objects.values('dept').distinct()
        dept_list = []
        for dept in depts:
            dept_list.append(dept['dept'])
        print(dept_list)
        return JsonResponse({
            'dept':dept_list
        })


# 查询按照要求的学生接口
class SearchCourse(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        dept = payload.get('dept')
        cno = payload.get('cno')
        cno_list = []
        cname_list = []
        teacher_list = []
        dept_list = []
        print(cno)
        if cno == '':
            if dept == '全部':
                courses = Course.objects.all()
            else:
                courses = Course.objects.filter(dept=dept)
        else:
            courses = Course.objects.filter(cno=cno)
        if not courses.exists():
            return HttpResponse('fail')

        for course in courses:
            cno_list.append(course.cno)
            cname_list.append(course.cname)
            teacher_list.append(course.teacher)
            dept_list.append(course.dept)
        # print(cno_list)
        return JsonResponse({
            'cno': cno_list,
            'cname': cname_list,
            'dept': dept_list,
            'teacher': teacher_list,
        })


# 更新学生信息接口
class UpdateCourseInfo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body)
        cno = payload.get('cno')
        cname = payload.get('cname')
        teacher = payload.get('teacher')
        dept = payload.get('dept')
        course = Course.objects.get(cno=cno)
        course.cname = cname
        course.teacher = teacher
        course.dept = dept
        course.save()
        # print(course)
        return HttpResponse('success')


# 管理员获取信息接口
class GetGradeInfo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        grades = Grade.objects.all()
        data = {'class':[],'dept':[]}
        sclasses = Students.objects.values('sclass').distinct()
        depts = Course.objects.values('dept').distinct()
        for sclass in sclasses:
            data['class'].append(sclass['sclass'])
        for dept in depts:
            data['dept'].append(dept['dept'])
        return JsonResponse({
            'data':data
        })


# 管理员修改成绩接口
class SearchGrade(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        payload = json.loads(request.body)
        # print(type(payload))
        print(payload)
        data = Grade.objects.all()
        # print(payload)
        for key in payload.keys():
            if payload[key] != '':
                if key == 'sno':
                    data = data.filter(sno=payload[key])
                if key == 'cno':
                    data = data.filter(cno=payload[key])
                if key == 'sclass':
                    snos = Students.objects.values('sno').filter(sclass=payload[key])
                    sno_list = []
                    # query_set
                    for sno in snos:
                        sno_list.append(sno['sno'])
                    # print(sno_list)
                    data = data.filter(sno__in=sno_list)
                    # print(data)
                if key == 'dept' or key == 'cname':
                    if key == 'dept':
                        cnos = Course.objects.values('cno').filter(dept=payload[key])
                    else:
                        # key == 'cname':
                        cnos = Course.objects.values('cno').filter(cname=payload[key])
                    cno_list = []
                    for cno in cnos:
                        cno_list.append(cno['cno'])
                    data = data.filter(cno__in=cno_list)
                # if key == 'cname':
            # print(data)
        if not data.exists():
            return HttpResponse('fail')
        else:
            info = {'sno':[],'sname':[],'cno':[],'cname':[],'grade':[]}
            for datum in data:
               student = datum.sno
               course =datum.cno
               info['sno'].append(student.sno)
               info['sname'].append(student.sname)
               info['cno'].append(course.cno)
               info['cname'].append(course.cname)
               if datum.grade == None:
                   info['grade'].append('无')
               else:
                   info['grade'].append(str(datum.grade))
            return JsonResponse({
                'data': info
            })


# 更新成绩信息接口
class UpdateGradeInfo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        payoad = json.loads(request.body)
        sno = payoad.get('sno')
        cno = payoad.get('cno')
        _grade = payoad.get('grade')
        # print(_grade)
        student = Students.objects.get(sno=sno)
        course = Course.objects.get(cno=cno)
        grade = Grade.objects.get(sno=student,cno=course)
        # print(grade)
        if _grade == '无':
            grade.grade = None
        else:
            grade.grade = _grade
        grade.save()
        return HttpResponse('修改成功')


# 查询学生班级接口
class SearchStudentClass(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        classes = Students.objects.values('sclass').distinct()
        class_list = []
        for sclass in classes:
            class_list.append(sclass['sclass'])
        # print(dept_list)
        return JsonResponse({
            'sclass':class_list
        })


# 管理员查询学生选课信息接口
class AdminChooseClassView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = json.loads(request.body) # payload is a dict

        student_info = {
            'sno':payload['sno'],
            'sname':payload['sname'],
            'sclass':payload['sclass']
        }

        course_info = {
            'cno':payload['cno'],
            'cname':payload['cname'],
            'dept':payload['dept']
        }
        # 筛选学生,课程,找出学号，课程号
        sno_list = []
        cno_list = []
        data = Students.objects.all()
        for keys in student_info.keys():
            if student_info[keys] != '':
                if keys == 'sno':
                    data = data.filter(sno=student_info[keys])
                if keys == 'sname':
                    data = data.filter(sname=student_info[keys])
                if keys == 'sclass':
                    data = data.filter(sclass=student_info['sclass'])

        for student in data:
            sno_list.append(student.sno)

        data = Course.objects.all()
        for keys in course_info.keys():
            if course_info[keys] != '':
                if keys == 'cno':
                    data = data.filter(cno=course_info[keys])
                if keys == 'cname':
                    data = data.filter(cname=course_info[keys])
                if keys == 'dept':
                    data = data.filter(dept=course_info['dept'])
        for course in data:
            cno_list.append(course.cno)

        data = {
            'sno':[],
            'sname':[],
            'cno':[],
            'cname':[],
            'dept':[],
            'teacher':[],
            'flag':[]
        }

        # 获得筛选的学生与课程，找出每个学生已获得成绩课程以及已选课程。
        students_chosen_course = []   # 学生已选择课程
        students_unchosen_course = [] # 学生未选择课程
        for sno in sno_list:
            student = Students.objects.filter(sno=sno)
            student_unchosen_course = []
            student_chosen_course = []
            for cno in cno_list:
                grades = Grade.objects.filter(sno=sno,cno=cno)
                if not grades.exists():
                    student_unchosen_course.append(cno)
                else:
                    for grade in grades:
                        if grade.grade is None:
                            student_chosen_course.append(cno)
            students_unchosen_course.append(student_unchosen_course)
            students_chosen_course.append(student_chosen_course)

        print(students_unchosen_course)
        print(students_chosen_course)

        data = {
            'sno':[],
            'sname':[],
            'cno':[],
            'cname':[],
            'dept':[],
            'teacher':[],
            'state':[],
        }
        i = 0
        for sno in sno_list:
            student = Students.objects.get(sno=sno)
            for cno in students_chosen_course[i]:
                course = Course.objects.get(cno=cno)
                data['sno'].append(student.sno)
                data['sname'].append(student.sname)
                data['cno'].append(course.cno)
                data['cname'].append(course.cname)
                data['dept'].append(course.dept)
                data['teacher'].append(course.teacher)
                data['state'].append(1)
            for cno in students_unchosen_course[i]:
                course = Course.objects.get(cno=cno)
                data['sno'].append(student.sno)
                data['sname'].append(student.sname)
                data['cno'].append(course.cno)
                data['cname'].append(course.cname)
                data['dept'].append(course.dept)
                data['teacher'].append(course.teacher)
                data['state'].append(0)
            i = i + 1

        # print(data)

        return JsonResponse({
            'data':data
        })


# 进行数据备份接口
class GetAllData(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        students = Students.objects.all()
        courses = Course.objects.all()
        grades = Grade.objects.all()
        data = {}
        student_info = {'sno':[],'sname':[],'sclass':[],'sex':[],'sage':[],'sdept':[]}
        course_info = {'cno':[],'cname':[],'dept':[],'teacher':[]}
        grade_info = {'sno':[],'cno':[],'grade':[]}
        for student in students:
            student_info['sno'].append(student.sno)
            student_info['sname'].append(student.sname)
            student_info['sclass'].append(student.sclass)
            student_info['sex'].append(student.sex)
            student_info['sage'].append(student.sage)
            student_info['sdept'].append(student.sdept)

        for course in courses:
            course_info['cno'].append(course.cno)
            course_info['cname'].append(course.cname)
            course_info['teacher'].append(course.teacher)
            course_info['dept'].append(course.dept)

        for grade in grades:
            student = grade.sno
            course = grade.cno
            grade_info['sno'].append(student.sno)
            grade_info['cno'].append(course.cno)
            grade_info['grade'].append(grade.grade)

        data['student'] = student_info
        data['course'] = course_info
        data['grade'] = grade_info
        #
        # data = json.dumps(data)
        # print(data)

        return JsonResponse({
            'data':data
        })
