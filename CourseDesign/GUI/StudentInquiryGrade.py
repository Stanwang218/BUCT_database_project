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
        # 设置标题与初始大小
        self.setWindowTitle('学生成绩查询')
        self.resize(800, 500)
        self.classedit = QLineEdit()
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(0, 5)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['课程号','课程名', '成绩', '开课学院', '老师'])

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
        choice_widget = QWidget()
        hbox_ = QHBoxLayout()
        form = QFormLayout()
        form.addRow('课程号',self.classedit)
        hbox_.addStretch(1)
        hbox_.addLayout(form)
        hbox_.addStretch(1)
        choice_widget.setLayout(hbox_)
        with open('data.json', 'r') as f:
            data = json.load(f)
        name = data['name']
        label = QLabel(name+"同学您好")
        layout.addWidget(label)
        layout.addWidget(choice_widget)
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

        #TODO 优化3 查询学生成绩
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['课程号', '课程名', '成绩', '开课学院', '老师'])
        url = 'http://127.0.0.1:8000/StudentGrade/'
        with open('data.json', 'r') as f:
            data = json.load(f)
            f.close()
        data['cno'] = self.classedit.text()
        data = json.dumps(data)
        # print(data)
        res = requests.post(url=url,data=data)
        result = res.json()
        # print(result)
        cname = result['cname']
        grade = result['grade']
        dept = result['dept']
        teacher = result['teacher']
        cno = result['cno']
        row = len(cname)
        if row == 0:
            QMessageBox.information(self,'提示信息','无查询信息')
        for i in range(row):
            self.model.appendRow([
                QStandardItem(cno[i]),
                QStandardItem(cname[i]),
                QStandardItem(str(grade[i])),
                QStandardItem(dept[i]),
                QStandardItem(teacher[i]),
            ])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = GradeTable()
    table.show()
    sys.exit(app.exec_())
