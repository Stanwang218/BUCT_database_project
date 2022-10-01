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
        self.labels = {
            '学号':'sno',
            '姓名':'sname',
            '课程号':'cno',
            '课程名': 'cname',
            '学生成绩': 'grade'
        }
        self.resize(500,300)
        self.initUI()

    def Myform(self,label,data):
        form = QFormLayout()
        if label == '学生成绩':
            line = QLineEdit()
            self.lines.append([self.labels[label],line])
            line.setText(data)
            form.addRow(label,line)
            return form
        line = QLabel(data)
        line.setText(data)
        form.addRow(label,line)
        return form

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        self.setWindowTitle('修改课程信息')
        vbox = QVBoxLayout()
        vbox.addLayout(self.Myform('学号',self.data['sno']))
        vbox.addLayout(self.Myform('姓名',self.data['sname']))
        vbox.addLayout(self.Myform('课程号',self.data['cno']))
        vbox.addLayout(self.Myform('课程名',self.data['cname']))
        vbox.addLayout(self.Myform('学生成绩',self.data['grade']))
        btn = QPushButton('修改')
        btn.clicked.connect(self.UpdateStudentInfo)
        vbox.addWidget(btn)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def UpdateStudentInfo(self):
        url = 'http://127.0.0.1:8000/UpdateGradeInfo/'
        data = {
            'cno':self.data['cno'],
            'sno':self.data['sno']
                }
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


class GradeInquiry(QWidget):
    def __init__(self):
        super(GradeInquiry, self).__init__()
        self.resize(800,700)
        # 部门以及课程号
        # 班级,学号,课程号
        self.deptcombobox = QComboBox()
        self.classcombobox = QComboBox()
        self.snolineedit = QLineEdit()
        self.cnolineedit = QLineEdit()
        self.cnamelineedit = QLineEdit()
        self.tablewidget = QTableWidget()
        self.initUI()

    def initUI(self):
        # tablewidget属性
        self.setWindowTitle("学生成绩信息查询")
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setHorizontalHeaderLabels(['学号','姓名','课程号', '课程名', '成绩','选项'])
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        #界面
        # 筛选条件:部门，性别，班级
        hbox_ = QHBoxLayout()
        form1 = QFormLayout()
        form2 = QFormLayout()
        hbox_.addStretch(1)
        form1.addRow('开课学院',self.deptcombobox)
        form2.addRow('班级',self.classcombobox)
        form1.addRow('学号',self.snolineedit)
        form2.addRow('课程号',self.cnolineedit)
        form1.addRow('课程名',self.cnamelineedit)
        # form3.addRow('班级',self.classcombobox)
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
        url = 'http://127.0.0.1:8000/GetGradeInfo/'
        data = requests.get(url=url)
        data = data.json()
        data = data['data']
        # print(data)
        dept_list = data['dept']
        dept_list = ['全部']+dept_list
        self.deptcombobox.addItems(dept_list)
        sclass_list = data['class']
        sclass_list = ['全部'] + sclass_list
        self.classcombobox.addItems(sclass_list)
        # post 请求查询dept

    def SearchURL(self):
        # 每次查询前得清空表 空结果的处理

        # 发送url
        url = 'http://127.0.0.1:8000/SearchGrade/'
        dept = self.deptcombobox.currentText()
        if dept == '全部':
            dept = ''
        sclass = self.classcombobox.currentText()
        if sclass == '全部':
            sclass = ''
        cno = self.cnolineedit.text()
        sno = self.snolineedit.text()
        cname = self.cnamelineedit.text()
        # print(cno)
        data = {
            'dept':dept,
            'sclass':sclass,
            'cno':cno,
            'sno':sno,
            'cname':cname
        }
        data = json.dumps(data)
        res = requests.post(url=url,data=data)
        # print(res.text)
        if res.text == 'fail':
            QMessageBox.information(self,'提示信息','无相关成绩信息，请重新查询')
            self.cnolineedit.setText('')
            self.cnamelineedit.setText('')
            self.snolineedit.setText('')
        else:
            result = res.json()
            print(result['data'])
            result = result['data']
            sno = result['sno']
            cno = result['cno']
            cname = result['cname']
            grade = result['grade']
            sname = result['sname']
            row = len(cno)
            self.tablewidget.setRowCount(row)
            for i in range(row):
                self.tablewidget.setItem(i, 0, QTableWidgetItem(sno[i]))
                self.tablewidget.setItem(i, 1, QTableWidgetItem(sname[i]))
                self.tablewidget.setItem(i, 2, QTableWidgetItem(cno[i]))
                self.tablewidget.setItem(i, 3, QTableWidgetItem(cname[i]))
                self.tablewidget.setItem(i, 4, QTableWidgetItem(grade[i]))
                data = {
                    'sno':sno[i],
                    'cno': cno[i],
                    'cname': cname[i],
                    'grade': grade[i],
                    'sname': sname[i],
                }
                btn = Mybutton(data)
                self.tablewidget.setCellWidget(i, 5, btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GradeInquiry()
    win.show()
    sys.exit(app.exec_())