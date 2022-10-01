import json
import os
import sys

import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Logout(QWidget):
    def __init__(self):
        super(Logout, self).__init__()
        self.resize(400,400)
        self.initUI()
        self.setcenter()

    def initUI(self):
        btn = QPushButton("退出登录")
        vbox = QVBoxLayout()
        vbox.addWidget(btn)
        btn.clicked.connect(self.PostURL)
        self.setLayout(vbox)

    def PostURL(self):
        url = 'http://127.0.0.1:8000/log_out/'
        with open('data.json', 'r') as f:
            data = json.load(f)
        print(data['token'])
        data = json.dumps(data)
        res = requests.post(url,data)
        result = res.text
        # print(result)

    def setcenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width() - size.width()) / 2
        newtop = (screen.height() - size.height()) / 2
        self.move(newleft, newtop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    OutWin = Logout()
    OutWin.show()
    sys.exit(app.exec_())