# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Desktop\WORK\Development\N900\900FTPClient\ui\openserver.ui'
#
# Created: Tue Jun 08 08:44:09 2010
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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 314, 781, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.m_bu_open_bookmarks = QtGui.QPushButton(self.layoutWidget)
        self.m_bu_open_bookmarks.setEnabled(True)
        self.m_bu_open_bookmarks.setObjectName("m_bu_open_bookmarks")
        self.gridLayout.addWidget(self.m_bu_open_bookmarks, 0, 0, 1, 1)
        self.m_bu_cancel = QtGui.QPushButton(self.layoutWidget)
        self.m_bu_cancel.setObjectName("m_bu_cancel")
        self.gridLayout.addWidget(self.m_bu_cancel, 0, 1, 1, 1)
        self.m_bu_connect = QtGui.QPushButton(self.layoutWidget)
        self.m_bu_connect.setObjectName("m_bu_connect")
        self.gridLayout.addWidget(self.m_bu_connect, 0, 2, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(self.centralWidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(9, 12, 781, 211))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.m_le_user = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_user.setText("")
        self.m_le_user.setObjectName("m_le_user")
        self.gridLayout_2.addWidget(self.m_le_user, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.m_le_password = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_password.setText("")
        self.m_le_password.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.m_le_password.setObjectName("m_le_password")
        self.gridLayout_2.addWidget(self.m_le_password, 2, 1, 1, 1)
        self.m_le_server = QtGui.QLineEdit(self.layoutWidget1)
        self.m_le_server.setText("")
        self.m_le_server.setObjectName("m_le_server")
        self.gridLayout_2.addWidget(self.m_le_server, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(20, 240, 721, 51))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "N900FTP-Open Location", None, QtGui.QApplication.UnicodeUTF8))
        self.m_bu_open_bookmarks.setText(QtGui.QApplication.translate("MainWindow", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.m_bu_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.m_bu_connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Enter your login credentials here, or open the bookmarks window", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

