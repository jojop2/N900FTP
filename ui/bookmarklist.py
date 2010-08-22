# -*- coding: utf-8 -*-

"""
Module implementing BookmarkList.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from helper.xmlbookmark import XmlBookmark
from helper.server import Server

from Ui_bookmarklist import Ui_MainWindow
from bookmarkedit import BookmarkEdit

class BookmarkList(QMainWindow, Ui_MainWindow):
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
		
		self.bookmarkEdit = BookmarkEdit(self)
		
		try :
			self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
			self.bookmarkEdit.setAttribute(Qt.WA_Maemo5StackedWindow, True)
			USE_MAEMO=True
		except :
			USE_MAEMO=False	
			
		self.m_lw_serverlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.m_lw_serverlist, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.openContextMenu)			
			
		self.serverList = None	
			
		self.xmlBookmark = XmlBookmark(self)
		self.readList()
		
    def readList(self):
		self.m_lw_serverlist.clear()
		if not self.xmlBookmark.initialize():
			QMessageBox.inform(self.parentWindow,  "FTP", "Bookmarklist can not be loaded")
			self.hide()
		self.serverList = self.xmlBookmark.getServerList()
		for i in self.serverList:
			self.m_lw_serverlist.addItem(i.name)
			
    def openContextMenu(self, point):
		entry = self.m_lw_serverlist.currentItem()
		servername = QString("")	
		menu = QMenu(self)	
		delAction=None
		if type(entry).__name__ != "NoneType":
			servername = entry.text()
			delAction = menu.addAction("Delete Bookmark")
		
		action = menu.exec_(self.mapToGlobal(point))
		if action == delAction:
			ret = QMessageBox.question(self,  "Bookmark Delete", "Do you really want to delete the bookmark?",  "",  "No")
			if ret == 0:
				if self.xmlBookmark.deleteServer(servername):
					self.readList()
    
    
    @pyqtSignature("")
    def on_m_bu_add_server_clicked(self):
		self.bookmarkEdit.show()
    
    @pyqtSignature("QModelIndex")
    def on_m_lw_serverlist_doubleClicked(self, index):
		entry = self.m_lw_serverlist.currentItem()
		servername = QString("")
		
		if type(entry).__name__ != "NoneType":
			servername = entry.text()
			server = self.xmlBookmark.getServer(servername)
			self.parentWindow.setServer(server)
			self.hide()
