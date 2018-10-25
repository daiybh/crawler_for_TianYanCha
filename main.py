
import sys

from PyQt5.QtWidgets import QApplication
import login


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = login.Loginwindow()
    w.show()
    sys.exit(app.exec_())
