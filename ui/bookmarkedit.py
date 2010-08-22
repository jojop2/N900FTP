# -*- coding: utf-8 -*-

"""
Module implementing BookmarkEdit.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignature

from Ui_bookmarkedit import Ui_MainWindow
from helper.xmlbookmark import XmlBookmark
from helper.server import Server

class BookmarkEdit(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
		"""
		Constructor
		"""
		QMainWindow.__init__(self, parent)
		self.parentWindow = parent
		self.setupUi(self)
		try :
			self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
			USE_MAEMO=True
		except :
			USE_MAEMO=False	
    
    @pyqtSignature("")
    def on_m_bu_cancel_clicked(self):
		self.m_le_servername.setText("")
		self.m_le_server.setText("")
		self.m_le_user.setText("")
		self.m_le_password.setText("")
		self.parentWindow
		self.hide()
    
    @pyqtSignature("")
    def on_m_bu_add_server_clicked(self):
		if self.m_le_servername.text() == "":
			QMessageBox.information(self,  "FTP",  "Enter a servername at least!")
			return
		newserv = Server(self.m_le_servername.text(), self.m_le_server.text(), self.m_le_user.text(),  self.m_le_password.text())
		xmlBookmark = XmlBookmark(self)
		if not xmlBookmark.initialize():
			QMessageBox.inform(self.parentWindow,  "FTP", "Bookmarklist can not be loaded")
		else:
			xmlBookmark.addServer(newserv)
		self.m_le_servername.setText("")
		self.m_le_server.setText("")
		self.m_le_user.setText("")
		self.m_le_password.setText("")
		self.parentWindow.readList()
		self.hide()
