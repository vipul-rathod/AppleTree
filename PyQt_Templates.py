import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *

class TemplateUI(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TemplateUI, self).__init__(parent)
        self.initUi()

    def initUi(self):
        #    Main layout
        mainLayout              =   QtGui.QVBoxLayout()
        butLabLayout            =   QtGui.QHBoxLayout()
        
        #    QLabel
        self.label              =   QtGui.QLabel('Hit Him:\t')
        butLabLayout.addWidget(self.label)
        
        #    QComboBox
        self.comboBox           =   QtGui.QComboBox()
        comboList               =   ['pushButton', 'comboBox']
        self.comboBox.addItems(comboList)
        mainLayout.addWidget(self.comboBox)

        #    QPushButton
        self.pushButton         =   QtGui.QPushButton("Hit Me!!!!!!!!")
        butLabLayout.addWidget(self.pushButton)
        mainLayout.addLayout(butLabLayout)
        
        #    QPlainTextEdit
        self.plainTextEdit      =   QtGui.QPlainTextEdit()
        mainLayout.addWidget(self.plainTextEdit)



        
        

        

        self.setLayout(mainLayout)
        self.setWindowTitle("Template")

if __name__ == '__main__':
    app  = QtGui.QApplication(sys.argv)
    temp = TemplateUI()
    temp.show()
    app.exec_()