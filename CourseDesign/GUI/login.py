import json
import os
import StudentAppCenter,TeacherAppCenter,AdminAppCenter
import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

path = 'material'


class LoginWin(QWidget):
    def __init__(self):
        super(LoginWin, self).__init__()
        self.loginButton = QPushButton("登录")
        self.loginButton.clicked.connect(self.PostURL)
        self.setWindowTitle("学生选课系统")
        self.resize(350, 150)
        self.form = QFormLayout()
        self.number = QLineEdit()
        self.password = QLineEdit()
        self.identity = QComboBox()
        self.SetUI()
        self.setStyleSheet(
            "LoginWin{background-color: #FFFFE0 }"
        )
        self.setcenter()

    def SetUI(self):
        self.loginButton.setStyleSheet(
            "loginButton{border-radius:20%;}QPushButton:hover{background:#66CCFF;})"
        )

        self.number.setPlaceholderText("用户名")
        pic1 = QPixmap(os.path.join(path, 'log_ic01.png'))
        label1 = QLabel()
        label1.setPixmap(pic1)

        self.password.setPlaceholderText("密码")
        self.password.setEchoMode(QLineEdit.Password)
        pic2 = QPixmap(os.path.join(path, 'log_ic02.png'))
        label2 = QLabel()
        label2.setPixmap(pic2)

        self.identity.addItems(['学生', '老师', '管理员'])

        self.form.addRow(label1, self.number)
        self.form.addRow(label2, self.password)
        self.form.addRow(self.identity, self.loginButton)

        self.setLayout(self.form)

    def setcenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width() - size.width()) / 2
        newtop = (screen.height() - size.height()) / 2
        self.move(newleft, newtop)

    def PostURL(self):
        sender = self.sender()
        url = 'http://127.0.0.1:8000/get_token/'
        # django处理url请求
        username = self.number.text()
        passwords = self.password.text()
        id = self.identity.currentIndex()
        data = {"username": username, "password": passwords, "identity": id}
        data = json.dumps(data)
        res = requests.post(url=url, data=data)
        result = res.json()
        print(result)
        if result['message'] == "fail":
            QMessageBox.critical(self,"提示信息","密码错误")
        else:
            with open('data.json', 'w') as f:
                json.dump(result,f)
            if id == 0:
                QMessageBox.information(self,"提示信息",result['name']+"同学您好")
                self.studentcenter = StudentAppCenter.StudentCenter()
                self.studentcenter.show()
                self.close()
            elif id == 1:
                QMessageBox.information(self,"提示信息",result['name']+"老师您好")
                self.techercenter = TeacherAppCenter.TeacherCenter()
                self.techercenter.show()
                self.close()
                # 查表 获得名字
            else:
                QMessageBox.information(self,"提示信息","管理员登录成功")
                self.admincenter = AdminAppCenter.AdminCenter()
                self.admincenter.show()
                self.close()

        # with open('data.json','r') as f:
        #     print(json.load(f))

