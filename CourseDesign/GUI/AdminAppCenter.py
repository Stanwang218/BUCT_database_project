from PyQt5.QtWidgets import *
import requests
import json
import sys
import login,StudentInquiry,CourseInquiry,GradeInquiry,AdminCourseChoice


class AdminCenter(QWidget):
    def __init__(self):
        super(AdminCenter, self).__init__()
        with open('data.json', 'r') as f:
            self.data = json.load(f)
        self.resize(500,600)
        self.initUI()
        self.setcenter()

    def initUI(self):
        v_box = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        label = QLabel("管理员您好")
        self.setWindowTitle("选课系统管理员端")
        vbox = QVBoxLayout()
        btn1 = QPushButton("学生信息管理")
        btn2 = QPushButton("课程信息管理")
        btn3 = QPushButton("成绩信息管理")
        btn4 = QPushButton("学生选课管理")
        btn5 = QPushButton("退出登录")
        btn6 = QPushButton("数据备份")
        btn1.clicked.connect(self.InquiryStudent)
        btn2.clicked.connect(self.ChooseClass)
        btn3.clicked.connect(self.InquiryGrade)
        btn4.clicked.connect(self.AdminCourse)
        btn5.clicked.connect(self.LogoutURL)
        btn6.clicked.connect(self.StoreTheData)
        v_box.addWidget(label)
        vbox.addStretch(1)
        vbox.addWidget(btn1)
        vbox.addStretch(1)
        vbox.addWidget(btn2)
        vbox.addStretch(1)
        vbox.addWidget(btn3)
        vbox.addStretch(1)
        vbox.addWidget(btn4)
        vbox.addStretch(1)
        vbox.addWidget(btn5)
        vbox.addStretch(1)
        vbox.addWidget(btn6)
        vbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        v_box.addLayout(hbox)
        self.setLayout(v_box)

    def setcenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width() - size.width()) / 2
        newtop = (screen.height() - size.height()) / 2
        self.move(newleft, newtop)

    def InquiryStudent(self):
        self.inquirystudent = StudentInquiry.StudentInquiry()
        self.inquirystudent.show()

    def ChooseClass(self):
        self.courseinquiry = CourseInquiry.CourseInquiry()
        self.courseinquiry.show()

    def InquiryGrade(self):
        self.gradeinquiry = GradeInquiry.GradeInquiry()
        self.gradeinquiry.show()

    def AdminCourse(self):
        self.admincourse = AdminCourseChoice.chooseclass()
        self.admincourse.show()

    def StoreTheData(self):
        choice = QMessageBox.information(self,'提示信息','是否确定进行数据备份',QMessageBox.Yes|QMessageBox.No)
        url = 'http://127.0.0.1:8000/GetAllData/'
        res = requests.get(url=url)
        result = res.json()
        result = result['data']
        if choice == QMessageBox.Yes:
            with open('students.txt', 'w') as f:
                json.dump(result['student'], f, ensure_ascii=False)
                f.close()
            with open('courses.txt', 'w') as f:
                json.dump(result['course'], f, ensure_ascii=False)
                f.close()
            with open('grades.txt', 'w') as f:
                json.dump(result['grade'], f, ensure_ascii=False)
                f.close()
            QMessageBox.information(self,'提示信息','数据已成功备份！')

    def LogoutURL(self):
        self.win = login.LoginWin()
        # 发送url删除token
        # print(self.data['token'])
        data = json.dumps(self.data)
        url = 'http://127.0.0.1:8000/log_out/'
        requests.post(url=url,data=data)
        self.close()
        self.win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    studentCenter = AdminCenter()
    studentCenter.show()
    sys.exit(app.exec_())