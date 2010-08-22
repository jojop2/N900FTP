# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Desktop\WORK\Development\N900\900FTPClient\ui\bookmarkedit.ui'
#
# Created: Tue Jun 08 21:50:27 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.layoutWidget = QtGui.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 340, 781, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.m_bu_cancel = QtGui.QPushButton(self.layoutWidget)
        self.m_bu_cancel.setObjectName("m_bu_cancel")
        self.gridLayout.addWidget(self.m_bu_cancel, 0, 0, 1, 1)
        self.m_bu_add_server = QtGui.QPushButton(self.layoutWidget)
        self.m_bu_add_server.setObjectName("m_bu_add_server")
        self.gridLayout.addWidget(self.m_bu_add_server, 0, 1, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(self.centralWidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 0, 771, 341))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.m_le_servername = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_servername.setText("")
        self.m_le_servername.setObjectName("m_le_servername")
        self.gridLayout_2.addWidget(self.m_le_servername, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.m_le_server = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_server.setText("")
        self.m_le_server.setObjectName("m_le_server")
        self.gridLayout_2.addWidget(self.m_le_server, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.m_le_user = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_user.setText("")
        self.m_le_user.setObjectName("m_le_user")
        self.gridLayout_2.addWidget(self.m_le_user, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.m_le_password = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_password.setText("")
        self.m_le_password.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.m_le_password.setObjectName("m_le_password")
        self.gridLayout_2.addWidget(self.m_le_password, 3, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "N900FTP-Open Location", None, QtGui.QApplication.UnicodeUTF8))
        self.m_bu_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.m_bu_add_server.setText(QtGui.QApplication.translate("MainWindow", "Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Bookmark-Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

