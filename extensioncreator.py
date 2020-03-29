import sys
from PyQt4 import QtGui, uic

class CreatorDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = uic.loadUi("extensioncreator.ui", self)
        

app = QtGui.QApplication(sys.argv)
dialog = CreatorDialog()
dialog.show()
sys.exit(app.exec_())
