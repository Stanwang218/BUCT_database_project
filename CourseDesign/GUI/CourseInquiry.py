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
        self.labels = {'课程名': 'cname', '开课教师': 'teacher',  '开课院系': 'dept'}
        self.resize(250,300)
        self.initUI()

    def Myform(self,label,data):
        form = QFormLayout()
        if label == '课程号':
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
        self.setWindowTitle('修改课程信息')
        vbox = QVBoxLayout()
        vbox.addLayout(self.Myform('课程号',self.data['cno']))
        vbox.addLayout(self.Myform('课程名',self.data['cname']))
        vbox.addLayout(self.Myform('开课教师',self.data['teacher']))
        vbox.addLayout(self.Myform('开课院系',self.data['dept']))
        btn = QPushButton('修改')
        btn.clicked.connect(self.UpdateStudentInfo)
        vbox.addWidget(btn)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def UpdateStudentInfo(self):
        url = 'http://127.0.0.1:8000/UpdateCourseInfo/'
        data = {'cno':self.data['cno']}
        for line in self.lines:
            data[line[0]] = line[1].text()
        data = json.dumps(data)
        choice = QMessageBox.information(self,'提示信息','确定更新？',QMessageBox.Yes | QMessageBox.No)
        # print(choice)
        if choice == QMessageBox.Yes:
            res = requests.post(url=url,data=data)
            QMessageBox.information(self,'提示信息','更新成功,请刷新')
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


class CourseInquiry(QWidget):
    def __init__(self):
        super(CourseInquiry, self).__init__()
        self.resize(800,700)
        # 部门以及课程号
        self.deptcombobox = QComboBox()
        self.lineedit = QLineEdit()
        self.tablewidget = QTableWidget()
        self.initUI()

    def initUI(self):
        # tablewidget属性
        self.setWindowTitle("课程信息查询")
        self.tablewidget.setColumnCount(5)
        self.tablewidget.setHorizontalHeaderLabels(['课程号', '课程名', '开课学院','教师','选项'])
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        #界面
        # 筛选条件:部门，性别，班级
        hbox_ = QHBoxLayout()
        form1 = QFormLayout()
        form2 = QFormLayout()
        hbox_.addStretch(1)
        form1.addRow('部门',self.deptcombobox)
        form2.addRow('课程号',self.lineedit)
        hbox_.addLayout(form1)
        hbox_.addLayout(form2)
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
        url = 'http://127.0.0.1:8000/SearchCourseDept/'
        data = requests.get(url=url)
        data = data.json()
        dept_list = data['dept']
        dept_list = ['全部']+dept_list
        self.deptcombobox.addItems(dept_list)
        # post 请求查询dept

    def SearchURL(self):
        # 每次查询前得清空表 空结果的处理

        # 发送url
        url = 'http://127.0.0.1:8000/SearchCourse/'
        dept = self.deptcombobox.currentText()
        cno = self.lineedit.text()
        print(cno)
        data = {
            'dept':dept,
            'cno':cno,
        }
        data = json.dumps(data)
        res = requests.post(url=url,data=data)
        # print(res.text)
        if res.text == 'fail':
            QMessageBox.information(self,'提示信息','无相关课程，请重新查询')
            self.lineedit.setText('')
        else:
            result = res.json()
            cno = result['cno']
            cname = result['cname']
            dept = result['dept']
            teacher = result['teacher']
            row = len(cno)
            self.tablewidget.setRowCount(row)
            for i in range(row):
                self.tablewidget.setItem(i, 0, QTableWidgetItem(cno[i]))
                self.tablewidget.setItem(i, 1, QTableWidgetItem(cname[i]))
                self.tablewidget.setItem(i, 2, QTableWidgetItem(dept[i]))
                self.tablewidget.setItem(i, 3, QTableWidgetItem(teacher[i]))
                data = {
                    'cno': cno[i],
                    'cname': cname[i],
                    'teacher': teacher[i],
                    'dept': dept[i],
                }
                btn = Mybutton(data)
                self.tablewidget.setCellWidget(i, 4, btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CourseInquiry()
    win.show()
    sys.exit(app.exec_())