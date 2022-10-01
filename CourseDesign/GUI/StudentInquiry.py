from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import os
import json
import sys


class UpdateWin(QWidget):
    def __init__(self,data):
        super(UpdateWin, self).__init__()
        self.data = data
        self.lines = []
        self.labels = {'姓名': 'sname', '性别': 'sex', '班级': 'sclass', '院系': 'dept'}
        self.resize(250,300)
        self.initUI()

    def Myform(self,label,data):
        form = QFormLayout()
        if label == '学号':
            line = QLabel(data)
            form.addRow(label,line)
            return form
        line = QLineEdit()
        self.lines.append([self.labels[label],line])
        line.setText(data)
        form.addRow(label,line)
        return form

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        self.setWindowTitle('修改学生信息')
        vbox = QVBoxLayout()
        vbox.addLayout(self.Myform('学号',self.data['sno']))
        vbox.addLayout(self.Myform('姓名',self.data['sname']))
        vbox.addLayout(self.Myform('性别',self.data['sex']))
        vbox.addLayout(self.Myform('班级',self.data['sclass']))
        vbox.addLayout(self.Myform('院系',self.data['dept']))
        btn = QPushButton('修改')
        btn.clicked.connect(self.UpdateStudentInfo)
        vbox.addWidget(btn)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def UpdateStudentInfo(self):
        url = 'http://127.0.0.1:8000/UpdateStudentInfo/'
        data = {'sno':self.data['sno']}
        flag = True
        for line in self.lines:
            if line[0] == 'sex':
                if line[1].text() == '男':
                    data[line[0]] = True
                elif line[1].text() == '女':
                    data[line[0]] = False
                else:
                    flag = False
            else:
                data[line[0]] = line[1].text()
        data = json.dumps(data)
        if flag is False:
            QMessageBox.information(self,'提示信息','性别有误')
        else:
            choice = QMessageBox.information(self, '提示信息', '确定更新？', QMessageBox.Yes | QMessageBox.No)
            # print(choice)
            if choice == QMessageBox.Yes:
                res = requests.post(url=url, data=data)
                QMessageBox.information(self, '提示信息', '更新成功,请刷新')
                self.close()


class Mybutton(QPushButton):
    def __init__(self,data):
        super(Mybutton, self).__init__()
        self.data = data
        self.setText('修改')
        self.clicked.connect(self.Cliked)

    # 选课以及退选发送url，1是已选课，0是未选课
    def Cliked(self):
        self.updatewin = UpdateWin(self.data)
        self.updatewin.show()


class StudentInquiry(QWidget):
    def __init__(self):
        super(StudentInquiry, self).__init__()
        self.resize(800,700)
        self.deptcombobox = QComboBox()
        self.sexcombobox = QComboBox()
        self.sexcombobox.addItems(['全部','男','女'])
        self.lineedit = QLineEdit()
        self.tablewidget = QTableWidget()
        self.initUI()

    def initUI(self):
        # tablewidget属性
        self.setWindowTitle("学生信息查询")
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setHorizontalHeaderLabels(['学号', '姓名', '性别','班级', '学院','选项'])
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        #界面
        # 筛选条件:部门，性别，班级
        hbox_ = QHBoxLayout()
        form1 = QFormLayout()
        form2 = QFormLayout()
        form3 = QFormLayout()
        hbox_.addStretch(1)
        form1.addRow('部门',self.deptcombobox)
        form2.addRow('班级',self.lineedit)
        form3.addRow('性别',self.sexcombobox)
        hbox_.addLayout(form1)
        hbox_.addLayout(form2)
        hbox_.addLayout(form3)
        hbox_.addStretch(1)
        layout = QVBoxLayout()
        layout.addLayout(hbox_)
        layout.addWidget(self.tablewidget)
        hbox = QHBoxLayout()
        widget = QWidget()
        btn = QPushButton("查询")
        btn.clicked.connect(self.SearchURL)
        btn1 = QPushButton("刷新")
        btn1.clicked.connect(self.SearchURL)
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(btn1)
        hbox.addStretch(1)
        widget.setLayout(hbox)
        layout.addWidget(widget)
        self.setLayout(layout)
        url = 'http://127.0.0.1:8000/SearchDept/'
        data = requests.get(url=url)
        data = data.json()
        dept_list = data['dept']
        dept_list = ['全部']+dept_list
        self.deptcombobox.addItems(dept_list)
        # post 请求查询dept

    def SearchURL(self):
        # 每次查询前得清空表 空结果的处理

        # 发送url
        url = 'http://127.0.0.1:8000/SearchStudent/'
        dept = self.deptcombobox.currentText()
        sclass = self.lineedit.text()
        sex = self.sexcombobox.currentIndex()
        if sex == 0:
            sex = 2
        elif sex == 1:
            sex = True
        else:
            sex = False
        data = {
            'dept':dept,
            'class':sclass,
            'sex':sex,
        }
        data = json.dumps(data)
        # print(type(data))
        res = requests.post(url=url,data=data)
        # print(res.text)
        result = res.json()
        sno = result['sno']
        sname = result['sname']
        dept = result['dept']
        sex = result['sex']
        sclass = result['class']
        row = len(sno)
        if row == 0:
            QMessageBox.information(self,'提示信息','未查询到任何学生信息')
        self.tablewidget.setRowCount(row)
        for i in range(row):
            self.tablewidget.setItem(i,0,QTableWidgetItem(sno[i]))
            self.tablewidget.setItem(i,1,QTableWidgetItem(sname[i]))
            self.tablewidget.setItem(i,2,QTableWidgetItem(sex[i]))
            self.tablewidget.setItem(i,3,QTableWidgetItem(sclass[i]))
            self.tablewidget.setItem(i,4,QTableWidgetItem(dept[i]))
            data = {
                'sno':sno[i],
                'sname':sname[i],
                'sex':sex[i],
                'sclass':sclass[i],
                'dept':dept[i],
            }
            btn = Mybutton(data)
            self.tablewidget.setCellWidget(i,5,btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentInquiry()
    win.show()
    sys.exit(app.exec_())