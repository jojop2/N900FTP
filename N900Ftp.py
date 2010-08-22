#!/usr/bin/env python

# N900FTP  v0.1a
# Author: Johannes Schwarz
# E-mail: n900ftp@dremadur.de

from PyQt4 import QtCore, QtGui

from ui.mainwindow import mMainWindow

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = mMainWindow(MainWindow)
    ui.show()
    sys.exit(app.exec_())
