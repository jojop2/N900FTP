# -*- coding: utf-8 -*-

"""
Module implementing OpenServer.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import Qt
from PyQt4.QtCore import *

from Ui_openserver import Ui_MainWindow
from bookmarklist import BookmarkList

from helper.server import Server

class OpenServer(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent):
		"""
		Constructor
		"""
		QMainWindow.__init__(self, parent)
		self.parentWindow = parent
		self.setupUi(self)
		
		self.bookmarklist = BookmarkList(self)
		
		try :
			self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
			self.bookmarklist.setAttribute(Qt.WA_Maemo5StackedWindow, True)
			USE_MAEMO=True
		except :
			USE_MAEMO=False	
		
    def setServer(self, server):
		self.m_le_password.setText(server.password)
		self.m_le_server.setText(server.server)
		self.m_le_user.setText(server.login)
    
    @pyqtSignature("")
    def on_m_bu_open_bookmarks_clicked(self):
		self.bookmarklist.show()		
    
    @pyqtSignature("")
    def on_m_bu_cancel_clicked(self):
		self.hide()
    
    @pyqtSignature("")
    def on_m_bu_connect_clicked(self):
        self.parentWindow.connectToServer(self.m_le_server.text(), self.m_le_user.text(),  self.m_le_password.text())
        self.hide()
		

