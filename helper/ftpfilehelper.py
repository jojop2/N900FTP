# N900FTP
# Author: Johannes Schwarz
# E-mail: n900ftp@dremadur.de


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui, QtNetwork	



class ftpFileHelper(QtCore.QObject):
    def __init__(self, server,  log,  pwd, parent=None):
		QObject.__init__(self, parent)
		
		self.pwidget = parent
		
		self.server = server
		self.login = log
		self.password = pwd
		
		self.ftphelper = QFtp(self)
		self.ftphelper.connectToHost(self.server)
		self.ftphelper.login(self.login, self.password)
		
		self.ftphelper.commandFinished.connect(self.ftpCommandFinished)
		self.ftphelper.listInfo.connect(self.fillRemoteDirList)
		
		self.currentLocalPath=''
		self.currentRemotePath=''
		
		self.mkDir =''
		
		self.outFile = None
		
		#1 = download all files in a directory
		#2= make dir on server
		self.action = 0
		
    def downloadFile(self, localPath,  remotePath,  remoteFileName):
		QDir(".").mkpath(localPath)
		self.outFile = QFile(localPath + remoteFileName)
		print "File "+remotePath+remoteFileName + " will be downloaded to "+localPath
		if not self.outFile.open(QtCore.QIODevice.ReadWrite):
			QtGui.QMessageBox.information(self.pwidget, "FTP",
			"Unable to save the file " +self.outFile.fileName())
		self.ftphelper.get(remotePath+"/"+remoteFileName,  self.outFile)
		
    def uploadFile(self, localFile,  remotePath):
		self.outFile = QFile(localFile)
		print "File "+ localFile + "will be uploaded to " + remotePath
		if not self.outFile.open(QtCore.QIODevice.ReadOnly):
			QtGui.QMessageBox.information(self.pwidget, "FTP",
			"Unable to upload the file "+self.outFile.fileName())
		self.ftphelper.put(self.outFile,  remotePath)
			
	
    def downloadFilesFromDirectory(self,  localPath,  remotePath):
		#action = 1 download Files in Directory
		self.action = 1
		self.currentLocalPath = localPath+"/"
		self.currentRemotePath=remotePath+"/"
		self.ftphelper.cd(self.currentRemotePath)
		self.ftphelper.list()
		
    def makeDirectoryOnServer(self,  baseRemotePath,  newDir):
		#action = 2 --> cd into baseRemotePath and then createNewDirectory
		self.action = 2
		self.mkDir = newDir
		print "makeDirectoryOnServer --> baseremotepath ="+baseRemotePath+"  new dir ="+newDir
		self.ftphelper.cd(baseRemotePath)
	
    def ftpCommandFinished(self, _, error):
        	
        if self.ftphelper.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(self.pwidget, "FTP", "Unable to connect to the FTP server.", self.ftphelper.errorString())
                return
            return

				
        if self.ftphelper.currentCommand() == QtNetwork.QFtp.Login:
            self.ftphelper.list()
		
		
#        if self.ftphelper.currentCommand() == QtNetwork.QFtp.Cd and self.action==1:
#			if error:
#				print self.ftphelper.errorString()
#			self.ftphelper.list()

        if self.ftphelper.currentCommand() == QtNetwork.QFtp.Get:
            if error:
                QMessageBox.information(self.pwidget, "FTP", "File couldn't be downloaded! "+ self.outFile.fileName())
                self.outFile.close()
                self.outFile.remove()
            else:
                print "File successfully downloaded!"
                self.outFile.close()
            self.outFile = None
            self.pwidget.changeLocalDirectory(".")
            self.ftphelper.close()
			
        if self.ftphelper.currentCommand() == QtNetwork.QFtp.Put:
            if error:
                QMessageBox.information(self.pwidget, "FTP", "File couldn't be uploaded!",  self.ftphelper.errorString())
                #print self.ftphelper.errorString()
                self.outFile.close()
                self.outFile.remove()
            else:
                print "File successfully uploaded!"
                self.outFile.close()
            self.outFile = None
            self.pwidget.changeRemoteDirectory(".")
            self.ftphelper.close()
			
		#We are in the remote dir and now we can create the new dir
        if self.ftphelper.currentCommand() == QtNetwork.QFtp.Cd and self.action == 2:
			if error:
				print "Cannot CD into directory "+self.mkDir +"   "+self.ftphelper.errorString()
			else:
				print "I cded into dir and now we can create the new one"+self.mkDir
				self.ftphelper.mkdir(self.mkDir)
			
		#We are in the remote dir and the new dir has been created
        if self.ftphelper.currentCommand() == QtNetwork.QFtp.Cd and self.action == 2:
			if error:
				print "New Dir creation failed! "+self.ftphelper.errorString()
			else :
				print "New Dir has been successfully created! "+self.mkDir
			self.action = 0	

				
 	
    def fillRemoteDirList(self,  ftpItem):
		#download all files in a directory when no symlink and readeable
		if self.action == 1 and ftpItem.isFile() and not ftpItem.isSymLink() and ftpItem.isReadable():	
			
			pl =1
			#Call the same class again, in order to download single files
			#print "DownloadFromDirectory file must be added: "+ftpItem.name()
			#print "Remotepath ="+self.currentRemotePath
			#print "Localepath ="+self.currentLocalPath
			
			ft = ftpFileHelper(self.server, self.login, self.password,  self.pwidget)
			ft.downloadFile(self.currentLocalPath+"/",  self.currentRemotePath,  ftpItem.name())
		if self.action == 1 and not ftpItem.isFile() and not ftpItem.isSymLink() and ftpItem.isReadable() and ftpItem.name()!="." and ftpItem.name()!="..":				
			#print "New Directory will be generated ="+self.currentLocalPath
			QDir(".").mkpath(self.currentLocalPath+"/"+ftpItem.name())
			self.ftphelper.close()

				
