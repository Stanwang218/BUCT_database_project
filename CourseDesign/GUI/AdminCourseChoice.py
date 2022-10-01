from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import os
import json
import sys


class Mybutton(QPushButton):
    def __init__(self,state,sno,cno):
        super(Mybutton, self).__init__()
        self.sno = sno
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
        data = {'sno': self.sno, 'cno': self.cno, 'state': self.state}
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
        self.resize(1000,500)

        self.snoline = QLineEdit()
        self.cnoline = QLineEdit()
        self.cname = QLineEdit()
        self.sname = QLineEdit()
        self.sclass = QComboBox()
        self.dept = QComboBox()

        self.tablewidget = QTableWidget()
        self.initUI()

    def initUI(self):
        # tablewidget属性
        self.setWindowTitle("选课管理")
        self.tablewidget.setColumnCount(7)
        # 学号，学生名，班级
        self.tablewidget.setHorizontalHeaderLabels(['学号','学生姓名','课程号','课程名','开课学院','教师','选项'])
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        #界面
        # 筛选条件4个line,2个combobox

        layout = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox_ = QHBoxLayout()
        hbox.addStretch(1)
        choice = QWidget()
        form1 = QFormLayout()
        form2 = QFormLayout()
        form3 = QFormLayout()
        form1.addRow('学号',self.snoline)
        form1.addRow('课程号',self.cnoline)
        form3.addRow('班级',self.sclass)
        form2.addRow('学生姓名',self.sname)
        form2.addRow('课程名',self.cname)
        form3.addRow('开课学院',self.dept)
        hbox_.addLayout(form1)
        hbox_.addLayout(form2)
        hbox_.addLayout(form3)
        hbox.addLayout(hbox_)
        hbox.addStretch(1)
        choice.setLayout(hbox)

        layout.addWidget(choice)
        layout.addWidget(self.tablewidget)
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

        url = 'http://127.0.0.1:8000/SearchStudentClass/'
        res = requests.get(url=url)
        result = res.json()
        class_list = result['sclass']
        class_list = ['全部']+class_list
        self.sclass.addItems(class_list)

        url = 'http://127.0.0.1:8000/SearchCourseDept/'
        res = requests.get(url=url)
        result = res.json()
        dept_list = result['dept']
        dept_list = ['全部'] + dept_list
        self.dept.addItems(dept_list)

    def ChooseClassURL(self):

        # 每次查询前得清空表 空结果的处理

        # 发送url

        # 筛选条件
        if self.sclass.currentText() == '全部':
            sclass = ''
        else:
            sclass = self.sclass.currentText()
        if self.dept.currentText() == '全部':
            dept = ''
        else:
            dept = self.dept.currentText()

        data = {
            'sno': self.snoline.text(),
            'sname': self.sname.text(),
            'sclass': sclass,
            'cno': self.cnoline.text(),
            'cname': self.cname.text(),
            'dept': dept,
        }

        url = 'http://127.0.0.1:8000/AdminChooseClassView/'
        data = json.dumps(data)   # 字符串
        # print(type(data))
        res = requests.post(url=url,data=data)
        # print(res.text)
        result = res.json()
        result = result['data']
        sno = result['sno']
        sname = result['sname']
        cno = result['cno']
        cname = result['cname']
        dept = result['dept']
        teacher = result['teacher']
        flag = result['state']
        row = len(cname)
        if row == 0:
            QMessageBox.information(self,'提示信息','无该选课信息')
            self.sname.setText('')
            self.snoline.setText('')
            self.cname.setText('')
            self.cnoline.setText('')
        else:
            self.tablewidget.setRowCount(row)
            for i in range(row):
                self.tablewidget.setItem(i, 0, QTableWidgetItem(sno[i]))
                self.tablewidget.setItem(i, 1, QTableWidgetItem(sname[i]))
                self.tablewidget.setItem(i, 2, QTableWidgetItem(cno[i]))
                self.tablewidget.setItem(i, 3, QTableWidgetItem(cname[i]))
                self.tablewidget.setItem(i, 4, QTableWidgetItem(dept[i]))
                self.tablewidget.setItem(i, 5, QTableWidgetItem(teacher[i]))
                datas = {'sno': sno[i], 'cno': cno[i], 'state': flag[i]}
                # print(datas)
                btn = Mybutton(flag[i], sno[i], cno[i])
                self.tablewidget.setCellWidget(i, 6, btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = chooseclass()
    win.show()
    sys.exit(app.exec_())