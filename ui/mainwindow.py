#!/usr/bin/env python

# -*- coding: utf-8 -*-

# N900FTP 
# Author: Johannes Schwarz
# E-mail: n900ftp@dremadur.de

"""
Module implementing MainWindow.
"""
import sys


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtNetwork

import ftplib
from ftplib import FTP

from collections import deque

import os
import os.path



from Ui_mainwindow import Ui_MainWindow
from openserver import OpenServer
#from openlocation import OpenLocation
#from ftpRecursiv import ftpRecursiv
from helper.ftpfilehelper import ftpFileHelper


class mMainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
  
    def __init__(self, parent = None):
		"""
		Constructor
		"""
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		
		#Add menu
		fremantle = self.menuBar().addMenu("Edit");
		openloc_act = fremantle.addAction("Open Location")
		QObject.connect(openloc_act, SIGNAL("triggered()"), self.openlocationWindow)
		switchlocdir_act = fremantle.addAction("Switch Locale Dir")
		QObject.connect(switchlocdir_act,  SIGNAL("triggered()"),  self.switchLocalDir)

		self.m_lw_local.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.m_lw_local, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.openLeftContextMenu)

		self.m_lw_remote.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.m_lw_remote, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.openRightContextMenu)

		try :
			self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
			USE_MAEMO=True
		except :
			USE_MAEMO=False	
			
		self.isLocalDirectory = {}		
		self.isRemoteDirectory = {}
		
		#Declare openLocation as StackedWindow
		self.openLocation=OpenServer(self)
		
		#self.localdir=QDir("/home/user/MyDocs")
		#self.localdir=QDir("c:")
		self.localdir=QDir().home()
		self.localPath=self.localdir.path()
		self.changeLocalDirectory(".")
		
			
		self.ftp = None
		self.outFile = None
		
		self.recftp = None
		
		#store local Directory e.g. /home/MyDocs
		self.currentLocalPath=self.localdir.path()
		#store remote Directory-Path  e.g. /home/sld/lkj
		self.currentRemotePath = QString("/")
		
		#the last piece of currentLocalPath
		self.currentLocalDir = QString("")
		#the latsw piece of currentRemotePath
		self.currentRemoteDir = QString("")
		
		#store local directory when starting an action
		self.startLocalPath=self.localdir.path()
		#store remote dirctory when starting an action
		self.startRemotePath = QString("")
		
		#actionRemotePath
		self.actionRemotePath=QString("")
		
		#for recursive stuff
		#self.pendingDirectories = deque()
		self.pendingDirectories = QStringList()
		self.startingDownloadRemoteDirectory=""
		
		self.ftpHelper = None
		
		self.server =""
		self.user =""
		self.pwd =""
		
    def switchLocalDir(self):
		self.backupLocalDir = self.localdir
		newDir = ""
		if self.localdir.path().startsWith("/home"):
			newDir = "/media/mmc1"
		else :
			newDir = QDir().home().path()
		(newDirSel,  ok) = QInputDialog.getText(self,  "Please enter new dir!",  "New Directory:",  QLineEdit.Normal,  newDir)
		if ok:
			self.localdir=QDir(newDirSel)
			self.currentLocalPath = self.localdir.path()
		self.changeLocalDirectory(".")

		
    def openLeftContextMenu(self, point):
		entry = self.m_lw_local.currentItem()
		file = QString("")
		
		menu = QMenu(self)
		
		#Is it a directory
		delDirAction = None
		delFileAction = None
		transferFile = None
		
		if type(entry).__name__ != "NoneType":
			file = entry.text()
			if entry.text()=="..":
				file = QString("")
			#A file is clicked 
			else:
				if self.ftp:
					transferFile = menu.addAction("Upload")
					menu.addSeparator()
				
				if self.isLocalDirectory.get(file):
					delDirAction = menu.addAction("Delete Directory")
				#so it must be a file
				else :
					delFileAction = menu.addAction("Delete File")
				renameAction = menu.addAction("Rename File ...")
				menu.addSeparator()
		
		newDirAction = menu.addAction("New Directory ...")
#		
		action = menu.exec_(self.mapToGlobal(point))
		if action == transferFile:
			if self.isLocalDirectory.get(file ):
				#print "Right Clicked on Dir "+file
				#print "CurrentLocalpath +file = "+self.currentLocalPath+"/"+file
				
				#We need to create the dir where the user clicked on
				#fh =ftpFileHelper(self.server, self.user, self.pwd,  self)
				#fh.makeDirectoryOnServer(self.currentRemotePath+"/",  file)
				ftplib_i = FTP(str(self.server))
				ftplib_i.login(str(self.user),  str(self.pwd))
				ftplib_i.cwd(str(self.currentRemotePath))
				try :
					ftplib_i.mkd(str(file))	
				except ftplib.error_perm, resp: 
					print "Directory exists already: "+file
				ftplib_i.quit()
				
				self.uploadDirectory(self.currentRemotePath, QDir(self.currentLocalPath+"/"+file))
#				if self.recftp:
#					self.recftp.abort()
#					self.recftp.deleteLater()
#					self.recftp = None
#				self.recftp =QFtp(self)
#				self.recftp.connectToHost(self.server)
#				self.recftp.login(self.user,  self.pwd)
#				self.recftp.commandFinished.connect(self.recftpCommandFinished)
#				self.recftp.listInfo.connect(self.recfillRemoteDirList)
#				self.recftp.done.connect(self.recftpDone)
#				print "TEST: "+self.currentRemotePath
#				self.actionRemotePath = self.currentRemotePath
#				self.startRemotePath = self.currentRemotePath+"/"
#				self.startLocalPath=self.currentLocalPath
#				#self.startingDownloadRemoteDirectory = self.currentRemotePath+"/"+file
#				self.pendingDirectories.append(self.currentRemotePath+"/"+file)
#				#self.pendingDirectories.append(self.startRemotePath)
#				#self.pendingDirectories.append(file)
#				print "added pending Directories "+file
#				self.processNextDirectory()
#
			#Upload one single file
			else :
				fh =ftpFileHelper(self.server, self.user, self.pwd,  self)
				fh.uploadFile(self.currentLocalPath+"/"+file,  self.currentRemotePath+"/"+file)
#		
		elif action == delFileAction:
			print "Deleting file "+file
			ret = QMessageBox.question(self,  "FTP Delete", "Do you really want to delete the file?",  "",  "No")
			if ret == 0:
				file = QFile(self.currentLocalPath+"/"+file)
				if file.remove():
					QMessageBox.information(self,  "FTP",  "File has been deleted successfully!")
				else:
					QMessageBox.information(self,  "FTP",  "File couldn't be deleted!")			
			self.changeLocalDirectory(".")		
					
		elif action == delDirAction:
			ret = QMessageBox.question(self,  "FTP Delete", "Do you really want to delete the directory and all subcontent?",  "",  "No")
			if ret == 0:			
				ga = os.popen("rm -rf "+str(self.currentLocalPath+"/"+file)).read()
				ga = ga.strip()#[11:]		
				print "Delete dir command="+ga.strip()
				self.changeLocalDirectory(".")

#		elif action == renameAction:
#			(newName,  ok) = QInputDialog.getText(self,  "Please enter new name!",  "New Filename:",  QLineEdit.Normal)
#			if ok:
#				self.ftp.rename(file, newName)
		elif action == newDirAction:
			(newDir,  ok) = QInputDialog.getText(self,  "Please enter new Directory!",  "New Directory:",  QLineEdit.Normal)
			if ok:
				curDir = QDir(self.currentLocalPath) 
				if (curDir.mkdir(newDir)):
					QMessageBox.information(self,  "FTP",  "New directory created!")			
				else :	
					QMessageBox.information(self,  "FTP",  "New directory couldn't be created!")	
			self.changeLocalDirectory(".")		
					
    def openRightContextMenu(self, point):
		entry = self.m_lw_remote.currentItem()
		file = QString("")
		
		menu = QMenu(self)
		
		#Is it a directory
		delDirAction = None
		delFileAction = None
		renameAction = None
		transferFile = None
		
		if type(entry).__name__ != "NoneType":
			file = entry.text()
			if entry.text()=="..":
				file = QString("")
			#A file is clicked 
			else:
				transferFile = menu.addAction("Download")
				menu.addSeparator()
				if self.isRemoteDirectory.get(file):
					delDirAction = menu.addAction("Delete Directory")
				#so it must be a file
				else :
					delFileAction = menu.addAction("Delete File")
				renameAction = menu.addAction("Rename File ...")
				menu.addSeparator()
		newDirAction = menu.addAction("New Directory ...")
		
		action = menu.exec_(self.mapToGlobal(point))
		if action == transferFile:
			if self.isRemoteDirectory.get(file ):
				if self.recftp:
					self.recftp.abort()
					self.recftp.deleteLater()
					self.recftp = None
				self.recftp =QFtp(self)
				self.recftp.connectToHost(self.server)
				self.recftp.login(self.user,  self.pwd)
				self.recftp.commandFinished.connect(self.recftpCommandFinished)
				self.recftp.listInfo.connect(self.recfillRemoteDirList)
				self.recftp.done.connect(self.recftpDone)
				self.actionRemotePath = self.currentRemotePath
				self.startRemotePath = self.currentRemotePath+"/"
				self.startLocalPath=self.currentLocalPath
				self.pendingDirectories.append(self.currentRemotePath+"/"+file)
				self.processNextDirectory()

			#Download one single file
			else :
				fh =ftpFileHelper(self.server, self.user, self.pwd,  self)
				fh.downloadFile(self.currentLocalPath+"/",  self.currentRemotePath,  file)
		
		elif action == delFileAction:
			print "Deleting file "+file
			ret = QMessageBox.question(self,  "FTP Delete", "Do you really want to delete the file?",  "",  "No")
			if ret == 0:
				self.ftp.remove(file)
		elif action == delDirAction:
			ret = QMessageBox.question(self,  "FTP Delete", "Do you really want to delete the directory and all subcontent?",  "",  "No")
			if ret == 0:			
				self.ftp.rmdir(file)
		elif action == renameAction:
			(newName,  ok) = QInputDialog.getText(self,  "Please enter new name!",  "New Filename:",  QLineEdit.Normal)
			if ok:
				self.ftp.rename(file, newName)
		elif action == newDirAction:
			(newDir,  ok) = QInputDialog.getText(self,  "Please enter new Directory!",  "New Directory:",  QLineEdit.Normal)
			if ok:
				self.ftp.mkdir(newDir)
		
    def uploadDirectory(self, baseremotePath,  dir):
		dir.setSorting(QDir.DirsFirst);
		dir.setFilter(QDir.Files | QDir.Dirs | QDir.NoSymLinks | QDir.NoDotAndDotDot)
		dirlist = dir.entryList(QDir.Dirs | QDir.NoSymLinks | QDir.NoDotAndDotDot)
		for i in dirlist:
			if i !="." and i!="..":
				#fh =ftpFileHelper(self.server, self.user, self.pwd,  self)
				#fh.makeDirectoryOnServer(baseremotePath+"/"+dir.dirName()+"/",  i)
				
				ftplib_i = FTP(str(self.server),  str(self.user),  str(self.pwd))
				#print "CD INTO "+baseremotePath+"/"+dir.dirName()+"/"
				ftplib_i = FTP(str(self.server))
				ftplib_i.login(str(self.user),  str(self.pwd))
				ftplib_i.cwd(str(baseremotePath+"/"+dir.dirName()+"/"))
				try :
					ftplib_i.mkd(str(i))	
				except ftplib.error_perm, resp: 
					print "Directory exists already: "+i 
				ftplib_i.quit()

				#self.changeRemoteDirectory(".")

				nextDir = QDir(dir.absolutePath()+"/"+i)
				self.uploadDirectory(baseremotePath+"/"+dir.dirName(),  nextDir)

		dir.setFilter(QDir.Files | QDir.Dirs | QDir.NoSymLinks | QDir.NoDotAndDotDot)
		dirlist = dir.entryList(QDir.Files| QDir.NoSymLinks)
		for i in dirlist:
			if i !="." and i!="..":
				print baseremotePath + " File ="+i
				fh =ftpFileHelper(self.server, self.user, self.pwd,  self)
				fh.uploadFile(dir.path()+"/"+i, baseremotePath+"/"+i)
		
			
    def removeDirRecursiv(self,  currentDir):
		#if Dir is not empty, go down and delete
        if not self.isRemoteDirEmpty(currentDir):
            print ""
        else :
            self.ftp.rmdir(currentDir)
		
	def isRemoteDirEmpty(self,  remDir):
		self.changeRemoteDirectory(remDir)
	
	#Open the StackedWindow to enter Login information
    def openlocationWindow(self):	
		self.openLocation.show()

	#Connect to Host with the login information
    def connectToServer(self, serverc,  userc,  pwdc):
        if self.ftp:
			self.ftp.abort()
			self.ftp.deleteLater()
			self.ftp=None
        self.m_lw_remote.clear()
        self.currentRemoteDir = QString("")
        self.currentRemotePath = QString("")
		
        self.server = serverc
        self.user = userc
        self.pwd = pwdc
		
        self.ftp = QFtp(self)
        self.ftp.connectToHost(self.server)
        self.ftp.login(self.user, self.pwd)
		
        self.ftp.commandFinished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.fillRemoteDirList)
        #self.ftp.done.connect(self.ftpDone)
        #self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)		

        self.m_lw_remote.clear()
        self.currentRemotePath = '/'
        self.isRemoteDirectory.clear()
		

    def ftpCommandFinished(self, _, error):
        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(self, "FTP", "Unable to connect to the FTP server.", self.ftp.errorString())
                #self.ftp.connectOrDisconnect()
                return
            return

        if self.ftp.currentCommand() == QtNetwork.QFtp.Login:
			if error:
				QtGui.QMessageBox.information(self, "FTP", "Unable to login.", self.ftp.errorString()) 
				return
			print "Connection established!"
			self.m_lw_remote.setEnabled(True)
			self.m_bu_disconnect.setEnabled(True)
			self.ftp.list()

        if self.ftp.currentCommand() == QtNetwork.QFtp.Get:
            if error:
                #self.statusLabel.setText("Canceled download of %s." % self.outFile.fileName())
                self.outFile.close()
                self.outFile.remove()
            else:
                #self.statusLabel.setText("Downloaded %s to current directory." % self.outFile.fileName())
                self.outFile.close()
                print "Yeah file successfully downloaded!"
            self.outFile = None
            #self.enableDownloadButton()
            #self.progressDialog.hide()
			
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            l1 = 1
			#if not self.isRemoteDirectory:
                #self.fileList.addTopLevelItem(QtGui.QTreeWidgetItem(["<empty>"]))
                #self.fileList.setEnabled(False)
				#m_lw_remote.addItem("<empty folder>")
				
        elif self.ftp.currentCommand() == QtNetwork.QFtp.Remove:
			   if error:
					QtGui.QMessageBox.information(self, "FTP", self.ftp.errorString())
			   else :
				   QtGui.QMessageBox.information(self, "FTP", "File successfully deleted!")
				   self.m_lw_remote.clear()
				   self.ftp.list()

        elif self.ftp.currentCommand() == QtNetwork.QFtp.Rmdir:
			   if error:
					QtGui.QMessageBox.information(self, "FTP", self.ftp.errorString())
			   else :
				   QtGui.QMessageBox.information(self, "FTP", "Directory successfully deleted!")
				   self.m_lw_remote.clear()
				   self.ftp.list()

        elif self.ftp.currentCommand() == QtNetwork.QFtp.Rename:
			if error:
				QtGui.QMessageBox.information(self,  "FTP",  self.ftp.errorString())
			else :
				QtGui.QMessageBox.information(self, "FTP", "File successfully renamed!")
				self.m_lw_remote.clear()
				self.ftp.list()
				
        elif self.ftp.currentCommand() == QtNetwork.QFtp.Mkdir:
			if error:
				QtGui.QMessageBox.information(self,  "FTP",  self.ftp.errorString())
			else :
				QtGui.QMessageBox.information(self, "FTP", "Directory successfully created!")
				self.m_lw_remote.clear()
				self.ftp.list()								
	
	#QFtp.list() was called, and now the data arrives line by line
    def fillRemoteDirList(self,  ftpItem):
		#if item is a directory
		if ftpItem.isDir():
			if ftpItem.name() != ".":
				self.isRemoteDirectory[ftpItem.name()]=ftpItem.isDir()
				self.m_lw_remote.addItem(QListWidgetItem(QIcon("ressource/folder.xpm"), ftpItem.name(), self.m_lw_remote))
		else :
			self.m_lw_remote.addItem(ftpItem.name())
    
   
    @pyqtSignature("QModelIndex")
    def on_m_lw_local_doubleClicked(self, index):
		self.changeLocalDirectory(self.m_lw_local.currentItem().text())
		
    def changeLocalDirectory(self,  newDir):
		#clear locallist first
		self.m_lw_local.clear()
		self.isLocalDirectory.clear()		
		#print "Before changing localeDir :"+self.currentLocalPath
		self.localdir.cd(newDir)
		#print "After changing localeDir :"+self.currentLocalPath
		
		self.currentLocalDir=newDir
		if  newDir!=".":
			self.currentLocalPath = self.localdir.path()
		
		#self.currentRemotePath = self.localdir.path()
		
		#add directories to the listwidget first together with an icon
		filelist = self.localdir.entryList(QDir.AllDirs)
		for i in filelist:
			if i == "..":
				self.m_lw_local.addItem(i)
			elif i != ".":
				self.m_lw_local.addItem(QListWidgetItem(QIcon("ressource/folder.xpm"), i, self.m_lw_local))
				self.isLocalDirectory[i]=1

		#now the normal files are added
		filelist = self.localdir.entryList(QDir.Files)
		for i in filelist:
			self.m_lw_local.addItem(i)		
    
    def changeRemoteDirectory(self,  newDir):
        #clear remotelist first
		self.m_lw_remote.clear()
		self.isRemoteDirectory.clear()
		
		#When parent Directory is selected, then cut away the last piece of self.currentRemotePath after the last /
		#/home/www/hello  --> .. --> /home/www/
		if newDir == "..":
			lastslash = self.currentRemotePath.lastIndexOf("/")
			self.currentRemotePath = self.currentRemotePath.mid(0, lastslash) 
		else :
			if self.currentRemotePath=="/":
				self.currentRemotePath+=newDir
			else :
				self.currentRemotePath += "/"+newDir
		#print "Change Remote path to"+self.currentRemotePath		
            
		self.currentRemoteDir = newDir
		#print "Current Remote dir is "+self.currentRemoteDir
		self.ftp.cd(self.currentRemoteDir)
		self.ftp.list()
	
    @pyqtSignature("QModelIndex")
    def on_m_lw_remote_doubleClicked(self, index):
		self.changeRemoteDirectory(self.m_lw_remote.currentItem().text())
    
    def processNextDirectory(self):
		if  self.pendingDirectories.count() > 0:
			#in pendingdirectories the whole path is listed which have to be processed  
			wholePath = self.pendingDirectories.takeFirst()
			#print "process: Whole Path :"+currentRemoteDiffDirectory
			
			lastIndexOfSlash = wholePath.lastIndexOf("/")
			self.actionRemotePath = wholePath
			#wholePath.mid(0, lastIndexOfSlash)
			self.currentRemoteDir = wholePath.mid(lastIndexOfSlash,  wholePath.size())
			
			#self.currentLocalDir = self.localdir.path() + help
			#print "process: actionRemotePath :"+self.actionRemotePath
			#print "process: CurrentLocalePath :"+self.currentLocalPath
			#print "process: StartRemotePath :"+self.startRemotePath
			#print "process: CurrentRemoteDir :"+self.currentRemoteDir
			#print "process: StartLocalPath :"+self.startLocalPath
			
			#get substring from actionRemotePath - startRemotePath
			substring = QString(self.actionRemotePath.mid(QString(self.startRemotePath).size(), self.actionRemotePath.size()))
			#print "process: Substring = "+substring
			
			ft = ftpFileHelper(self.server,  self.user, self.pwd,  self)
			ft.downloadFilesFromDirectory(self.startLocalPath+"/"+substring,  self.actionRemotePath)
			
			
			#self.m_lw_remote.clear()
			self.recftp.cd(self.actionRemotePath)
			self.recftp.list()

    def recftpCommandFinished(self, error):
		#print "Command Finished"
		l=1
		
    def recfillRemoteDirList(self, urlInfo):
        if urlInfo.isDir() and not urlInfo.isSymLink() and urlInfo.name() != "." and urlInfo.name() != "..":
            #print "Add to pending "+self.actionRemotePath+"/"+urlInfo.name()	
            self.pendingDirectories.append(self.actionRemotePath+"/"+urlInfo.name())
		
    def recftpDone(self,  error):
		if error:
			QMessageBox.information(self,  "FTP",  self.ftp.errorString())
		#else :
			#QMessageBox.information(self,  "FTP",  "Download Finished")aa
		self.processNextDirectory()		
    
    @pyqtSignature("")
    def on_m_bu_disconnect_clicked(self):
        if self.ftp:
			self.ftp.abort()
			self.ftp.deleteLater()
			self.ftp=None
        self.m_lw_remote.clear()
        self.currentRemoteDir = QString("")
        self.currentRemotePath = QString("")
        self.m_bu_disconnect.setEnabled(False)
		
