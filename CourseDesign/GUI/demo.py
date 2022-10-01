from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import os
import json
import sys


class Mybutton(QPushButton):
    def __init__(self):
        super(Mybutton, self).__init__()
        self.setText("选课")
        self.clicked.connect(self.Cliked)

    # 选课以及退选发送url
    def Cliked(self):
        if self.text() == "选课":
            self.setText("退选")
        else:
            self.setText("选课")


class chooseclass(QWidget):
    def __init__(self):
        super(chooseclass, self).__init__()
        self.resize(800,800)
        self.tablewidget = QTableWidget()
        self.initUI()

    def initUI(self):
        # tablewidget属性
        self.setWindowTitle("学生选课")
        layout = QVBoxLayout()
        layout.addWidget(self.tablewidget)
        self.tablewidget.setColumnCount(5)
        self.tablewidget.setHorizontalHeaderLabels(['课程号','课程名','开课学院','教师','选项'])
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #界面
        # 筛选条件。。。。
        widget = QWidget()
        hbox = QHBoxLayout()
        btn = QPushButton("查询")
        btn.clicked.connect(self.ChooseClassURL)
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        widget.setLayout(hbox)
        layout.addWidget(widget)
        self.setLayout(layout)

    def ChooseClassURL(self):
        # 每次查询前得清空表

        # 发送url
        url = 'http://127.0.0.1:8000/StudentChooseClass/'
        with open('data.json', 'r') as f:
            data = json.load(f)
        data = json.dumps(data)
        # print(data)
        res = requests.post(url=url,data=data)
        print(res.text)
        result = res.json()
        cno = result['cno']
        cname = result['cname']
        dept = result['dept']
        teacher = result['teacher']
        row = len(cname)
        self.tablewidget.setRowCount(row)
        for i in range(row):
            self.tablewidget.setItem(i,0,QTableWidgetItem(cno[i]))
            self.tablewidget.setItem(i,1,QTableWidgetItem(cname[i]))
            self.tablewidget.setItem(i,2,QTableWidgetItem(dept[i]))
            self.tablewidget.setItem(i,3,QTableWidgetItem(teacher[i]))
            btn = Mybutton()
            self.tablewidget.setCellWidget(i,4,btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = chooseclass()
    win.show()
    sys.exit(app.exec_())