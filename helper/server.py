# N900FTP
# Author: Johannes Schwarz
# E-mail: n900ftp@dremadur.de


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui

class Server(QtCore.QObject):
	def __init__(self, namei,  serverI,  log,  pwd, parent=None):
		QObject.__init__(self, parent)
		
		self.name = namei
		self.server = serverI
		self.login = log
		self.password = pwd
