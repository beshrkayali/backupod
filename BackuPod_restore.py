import gtk
import zipfile
import os
import shutil
# additional
import BackuPod_shared

def createDirs(path):
	pathList = path.split("/")
	dirsList = []
	tempVal = ""
	for i in range(0,len(pathList)):
		currPath = pathList[i]
		if tempVal == "":
			tempVal = currPath + "/"
		else:
			if i == len(pathList)-1:
				tempVal = tempVal + currPath
			else:
				tempVal = tempVal + currPath + "/"
		dirsList.append(tempVal)
	for dirItem in dirsList:
		if os.path.exists(dirItem) == False:
			#print dirItem.split(".")
			if len(dirItem.split(".")) <= 1:
				if dirItem[dirItem.rfind("/"):len(dirItem)] == "/":
					os.mkdir(dirItem)
	
def RestoreiPod(self,podPath):
	loadDialog = gtk.FileChooserDialog("Select Backup File to Restore", self.wTree.get_widget("BackuPodForm"), gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	loadDialogFilter = gtk.FileFilter()
	loadDialogFilter.set_name("iPod Backup File")
	loadDialogFilter.add_pattern("*.ipb")
	loadDialog.add_filter(loadDialogFilter)
	loadDialog.show()
	response = loadDialog.run()
	if response == gtk.RESPONSE_CANCEL:
		loadDialog.destroy()
	elif response == gtk.RESPONSE_OK:
		savedBackup = loadDialog.get_filename()
		loadDialog.destroy()
		backupFile = zipfile.ZipFile(savedBackup,"r")
		respond, dialog = BackuPod_shared.getAnswer("WARNING!","Restoring this backup file to your iPod will ERASE ALL YOUR MUSIC LIBRARY, if you are not sure please don't proceed.\nDo you want to continue?")
		if respond == gtk.RESPONSE_YES:
			if podPath[len(podPath)-2:len(podPath)-1]:
				podPath += "/"
			shutil.rmtree(podPath + "iPod_Control")
			os.mkdir(podPath + "iPod_Control")
			print "Working....."
			for filename in backupFile.namelist():
				if filename != "library.lib":
					storingPath = filename[filename.find("iPod_Control"):len(filename)]
					storingPodPath = podPath + storingPath
					if storingPodPath[len(storingPath)-1:len(storingPath)] != "/":
						createDirs(storingPodPath)
						file(storingPodPath, 'wb').write(backupFile.read(filename))
			print "Restore completed."
			BackuPod_shared.MessageBox("Restore Completed.","BackuPod finished restoring your iPod.")
			self.wTree.get_widget("StatusBar").push(self.statusContext, "iPod Restored.")
		dialog.destroy()
def Restore(self):
	iPodPath = BackuPod_shared.getipodPath()
	if iPodPath != None:
		RestoreiPod(self,iPodPath)
