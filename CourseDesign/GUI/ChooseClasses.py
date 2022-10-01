from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import os
import json
import sys


class Mybutton(QPushButton):
    def __init__(self,state,username,cno):
        super(Mybutton, self).__init__()
        self.username = username
        self.state = state
        self.cno = cno
        # print(self.username)
        # print(self.state)
        # print(self.cno)
        if self.state == 1:
            self.setText("退课")
            self.setStyleSheet('Mybutton{background-color:#f08080}')
        else:
            self.setText("选课")
            self.setStyleSheet('Mybutton{background-color:#00ccff}')
        self.clicked.connect(self.Cliked)

    # 选课以及退选发送url，1是已选课，0是未选课
    def Cliked(self):
        data = {'sno': self.username, 'cno': self.cno, 'state': self.state}
        if self.state == 1:
            #已经选课
            choice = QMessageBox.information(self,'提示信息','是否退课',QMessageBox.Yes|QMessageBox.No)
            if choice == QMessageBox.Yes:
                data = json.dumps(data)
                url = 'http://127.0.0.1:8000/StudentChooseClassUtility/'
                res = requests.post(url=url, data=data)
                # print(res.text)
                self.setText("选课")
                self.setStyleSheet('Mybutton{background-color:#00ccff}')
                self.state = 0
                QMessageBox.information(self,'提示信息','退课成功')
                # print(data)
        elif self.state == 0:
            choice = QMessageBox.information(self, '提示信息', '是否选课', QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                data = json.dumps(data)
                url = 'http://127.0.0.1:8000/StudentChooseClassUtility/'
                res = requests.post(url=url, data=data)
                # print(res.text)
                self.setText("退课")
                self.setStyleSheet('Mybutton{background-color:#f08080}')
                self.state = 1
                QMessageBox.information(self,'提示信息','选课成功')
                # print(data)


class chooseclass(QWidget):
    def __init__(self):
        super(chooseclass, self).__init__()
        self.resize(800,500)
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
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

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
        # 每次查询前得清空表 空结果的处理

        # 发送url
        url = 'http://127.0.0.1:8000/StudentChooseClass/'
        with open('data.json', 'r') as f:
            data = json.load(f)
            # 字典
        username = data['username']
        data = json.dumps(data) # 字符串
        # print(type(data))
        res = requests.post(url=url,data=data)
        # print(res.text)
        result = res.json()
        cno = result['cno']
        cname = result['cname']
        dept = result['dept']
        teacher = result['teacher']
        flag = result['state']
        row = len(cname)
        self.tablewidget.setRowCount(row)
        for i in range(row):
            self.tablewidget.setItem(i,0,QTableWidgetItem(cno[i]))
            self.tablewidget.setItem(i,1,QTableWidgetItem(cname[i]))
            self.tablewidget.setItem(i,2,QTableWidgetItem(dept[i]))
            self.tablewidget.setItem(i,3,QTableWidgetItem(teacher[i]))
            # datas = {'sno':username,'cno':cno[i],'state':flag[i]}
            # print(datas)
            btn = Mybutton(flag[i],username,cno[i])
            self.tablewidget.setCellWidget(i,4,btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = chooseclass()
    win.show()
    sys.exit(app.exec_())