from PyQt5.QtWidgets import *
import requests
import json
import sys
import login,CreateClasses,TeacherInquryGrade


class TeacherCenter(QWidget):
    def __init__(self):
        super(TeacherCenter, self).__init__()
        with open('data.json', 'r') as f:
            self.data = json.load(f)
        self.resize(400,400)
        self.initUI()
        self.setcenter()

    def initUI(self):
        v_box = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        label = QLabel(self.data['name']+"老师您好")
        self.setWindowTitle("选课系统教师端")
        vbox = QVBoxLayout()
        btn1 = QPushButton("开设课程")
        btn2 = QPushButton("查看选课学生")
        btn3 = QPushButton("退出登录")
        btn1.clicked.connect(self.CreateClass)
        btn2.clicked.connect(self.InquiryGrade)
        btn3.clicked.connect(self.LogoutURL)
        v_box.addWidget(label)
        vbox.addStretch(1)
        vbox.addWidget(btn1)
        vbox.addStretch(1)
        vbox.addWidget(btn2)
        vbox.addStretch(1)
        vbox.addWidget(btn3)
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

    def InquiryGrade(self):
        self.inquirygrade = TeacherInquryGrade.GradeTable()
        self.inquirygrade.show()

    def CreateClass(self):
        self.createclass = CreateClasses.CreateCenter()
        self.createclass.show()

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
    teacherCenter = TeacherCenter()
    teacherCenter.show()
    sys.exit(app.exec_())