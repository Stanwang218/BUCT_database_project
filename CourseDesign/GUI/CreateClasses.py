from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import os
import json
import sys


class CreateCenter(QWidget):
    def __init__(self):
        super(CreateCenter, self).__init__()
        self.cno_line = QLineEdit()
        self.cname_line = QLineEdit()
        self.dept_line = QLineEdit()
        self.initUI()
        self.setWindowTitle("创建新课程")
        self.resize(400,400)
        self.setcenter()

    def initUI(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        form1 = QFormLayout()
        form2 = QFormLayout()
        form3 = QFormLayout()
        btn = QPushButton("确定")
        btn.clicked.connect(self.CreatePost)
        form1.addRow("课程号",self.cno_line)
        form2.addRow("课程名",self.cname_line)
        form3.addRow("开课院系",self.dept_line)
        vbox.addLayout(form1)
        vbox.addStretch(1)
        vbox.addLayout(form2)
        vbox.addStretch(1)
        vbox.addLayout(form3)
        vbox.addStretch(1)
        vbox.addWidget(btn)
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def CreatePost(self):
        with open('data.json', 'r') as f:
            json_data = json.load(f)
        name = json_data["name"]

        data = {
            'cno':self.cno_line.text(),
            'cname':self.cname_line.text(),
            'dept':self.dept_line.text(),
            'name':name,
        }
        data = json.dumps(data)
        url = 'http://127.0.0.1:8000/CreateClass/'
        res = requests.post(url=url,data=data)
        result = res.text
        if result == "success":
            QMessageBox.information(self,"提示信息",self.cname_line.text()+"课程创建成功")
        else:
            QMessageBox.information(self, "提示信息", "课程号重复,课程创建失败")
        self.cname_line.setText("")
        self.dept_line.setText("")
        self.cno_line.setText("")

    def setcenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width() - size.width()) / 2
        newtop = (screen.height() - size.height()) / 2
        self.move(newleft, newtop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    createcenter = CreateCenter()
    createcenter.show()
    sys.exit(app.exec_())