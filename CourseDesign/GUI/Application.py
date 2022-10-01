import login
import sys
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Windows = login.LoginWin()
    Windows.show()
    sys.exit(app.exec_())