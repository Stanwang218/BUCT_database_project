from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import os
import json
import sys


class GradeTable(QWidget):
    def __init__(self, parent=None):
        super(GradeTable, self).__init__(parent)
        self.classes = QLineEdit()
        self.combobox = QComboBox()
        with open('data.json', 'r') as f:
            self.data = json.load(f)
            f.close()
        # 设置标题与初始大小
        self.setWindowTitle('教师查询成绩')
        self.resize(800, 500)

        # 设置数据层次结构，0行6列
        self.model = QStandardItemModel(0, 7)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['课程号','课程名','学号', '姓名', '班级', '学院','成绩'])

        # 实例化表格视图，设置模型为自定义的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # todo 优化1 表格填满窗口

        # 水平方向列自动拉伸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)

        # 水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 只能选一个单元格
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        # 选取一整行
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 无法编辑
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)

        # 设置布局
        layout = QVBoxLayout()
        with open('data.json', 'r') as f:
            data = json.load(f)
        name = data['name']
        # 插入选择的条件
        label = QLabel(name + "老师您好")
        layout.addWidget(label)
        layout.addLayout(self.attributeLine())
        layout.addWidget(self.tableView)
        widget = QWidget()
        hbox = QHBoxLayout()
        btn = QPushButton("查询")
        btn.clicked.connect(self.inquiryGrade)
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        widget.setLayout(hbox)
        layout.addWidget(widget)
        self.setLayout(layout)

    def inquiryGrade(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['课程号','课程名','学号', '姓名', '班级', '学院', '成绩'])
        url = 'http://127.0.0.1:8000/TeacherSearchGrade/'
        coursename = self.combobox.currentText()
        student_class = self.classes.text()
        data = {
            'teacher':self.data['name'],
            'cname':coursename,
            'sclass':student_class,
        }
        data = json.dumps(data)
        # print(data)
        res = requests.post(url=url, data=data)
        result = res.json()
        # print(result)
        cno = result['cno']
        sno = result['sno']
        sname = result['name']
        grade = result['grade']
        dept = result['dept']
        sclass = result['class']
        cname = result['cname']
        row = len(sno)
        if row == 0:
            data = self.combobox.currentText()
            if data != '全部':
                QMessageBox.information(self,'提示信息','该条件下，'+data+'无选课信息')
            else:
                QMessageBox.information(self,'提示信息','无任何选课信息')
            self.classes.setText('')
        for i in range(row):
            self.model.appendRow([
                QStandardItem(cno[i]),
                QStandardItem(cname[i]),
                QStandardItem(sno[i]),
                QStandardItem(sname[i]),
                QStandardItem(sclass[i]),
                QStandardItem(dept[i]),
                QStandardItem(str(grade[i])),
            ])

    def attributeLine(self):
        # 按照学科，班级，
        hbox = QHBoxLayout()
        hbox_ = QHBoxLayout()
        form1 = QFormLayout()
        form2 = QFormLayout()
        form1.addRow('课程',self.combobox)
        form2.addRow('班级',self.classes)
        hbox_.addLayout(form1)
        hbox_.addLayout(form2)
        hbox.addStretch(1)
        hbox.addLayout(hbox_)
        hbox.addStretch(1)
        # 获取帐号
        data = json.dumps(self.data)
        url = 'http://127.0.0.1:8000/SearchClass/'
        res = requests.post(url=url, data=data)
        result = res.json()
        course_name = result['course']
        if course_name is None:
            QMessageBox.warning(self, "提示信息", "老师您还没有开课！")
        else:
            course_name = ['全部'] + course_name
            self.combobox.addItems(course_name)
        return hbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = GradeTable()
    table.show()
    sys.exit(app.exec_())
