# N900FTP
# Author: Johannes Schwarz
# E-mail: n900ftp@dremadur.de


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtNetwork,  QtXml

from helper.server import Server



class XmlBookmark(QtCore.QObject):
	def __init__(self, parent=None):
		QtCore.QObject.__init__(self, parent)
		
		self.root = None
		
		self.doc =QtXml.QDomDocument("Bookmarks")
		
		self.bookmarkdir = QDir(QDir().home().path()+"/.n900ftp")
		self.bookmarkdir.mkpath(self.bookmarkdir.path())
		
		print self.bookmarkdir.path()+"/bookmarks.xml"
		
		self.file = QFile(self.bookmarkdir.path()+"/bookmarks.xml")
		
	def initialize(self):
		if not self.file.exists():
			print "Bookmark file does not exist and will be created now!"
			root = self.doc.createElement("Bookmarks")
			self.doc.appendChild(root)
			if not self.file.open(QtCore.QIODevice.ReadWrite):
				return False
			ts = QTextStream(self.file)
			ts << self.doc.toString()
			self.file.close()
			self.flushFile()

		
		if not self.file.open(QtCore.QIODevice.ReadWrite):
			self.file.close()
			return False
		if not self.doc.setContent(self.file):
			self.file.close()
			return False
		self.file.close()
					
		self.root = self.doc.documentElement()
		print self.root.tagName()			
		if self.root.tagName() != "Bookmarks":
			return False
		return True
	
	def flushFile(self):
		if not self.file.open(QtCore.QIODevice.WriteOnly):
			return False
		ts = QTextStream(self.file)
		ts << self.doc.toString()
		self.file.close()
		return True
			
	def deleteServer(self,  servername):
		domNode = self.root.firstChild()
		while not domNode.isNull():
			domElement = domNode.toElement()
			if not domElement.isNull():
				if domElement.tagName() == "Server":
					name = domElement.attribute("name",  "")
					if name == servername:
						self.root.removeChild(domElement)
						self.flushFile()
						return True
						break

			domNode = domNode.nextSibling()
		return False
			
	def addServer(self,  server):
		serv = self.doc.createElement("Server")
		serv.setAttribute("name",  server.name)
		serv.setAttribute("server",  server.server)
		serv.setAttribute("login",  server.login)
		serv.setAttribute("password",  server.password)
		
		self.root.appendChild(serv)
		
		self.flushFile()
			
#		if not self.file.open(QtCore.QIODevice.ReadWrite):
#			return -1
#		if not self.doc.setContent(self.file):
#			self.file.close()
#			return -2
#		self.file.close()

	def getServerList(self):
		serverList =[]
		domNode = self.root.firstChild()
		while not domNode.isNull():
			domElement = domNode.toElement()
			if not domElement.isNull():
				if domElement.tagName() == "Server":
					name = domElement.attribute("name",  "")
					server = domElement.attribute("server", "")
					login = domElement.attribute("login",  "")
					password = domElement.attribute("password",  "")
					serv = Server(name,  server,  login,  password)
					serverList.append(serv)
			domNode = domNode.nextSibling()
		return serverList

	def getServer(self,  servername):
		domNode = self.root.firstChild()
		while not domNode.isNull():
			domElement = domNode.toElement()
			if not domElement.isNull():
				if domElement.tagName() == "Server":
					name = domElement.attribute("name",  "")
					if name == servername:
						server = domElement.attribute("server", "")
						login = domElement.attribute("login",  "")
						password = domElement.attribute("password",  "")
						serv = Server(name,  server,  login,  password)
						return serv
			domNode = domNode.nextSibling()
		return Server("",  "",  "",  "")
