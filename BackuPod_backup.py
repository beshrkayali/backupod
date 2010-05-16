import os
import gtk
import encodings
import zipfile

from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4

# additional
import BackuPod_shared


def listiPodControl(Path):
	filesList = []
	iPod_Control = os.listdir(Path)
	for folder in iPod_Control:
		if os.path.isdir(Path + "/" + folder):
			subFolders = os.listdir(Path + "/" + folder)
			for fileORfolder in subFolders:
				if os.path.isdir(Path + "/" + folder + "/" +  fileORfolder):
					songsDirs = os.listdir(Path + "/" + folder + "/" +  fileORfolder)
					for song in songsDirs:
						filesList.append(Path + "/" + folder + "/" +  fileORfolder + "/" + song)
				else:
					filesList.append(Path + "/" + folder + "/" +  fileORfolder)
	return filesList

def CreateBackup(self,podPath):
	saveDialog = gtk.FileChooserDialog("Save your Backup File", self.wTree.get_widget("BackuPodForm"), gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
	saveDialogFilter = gtk.FileFilter()
	saveDialogFilter.set_name("iPod Backup File")
	saveDialogFilter.add_pattern("*.ipb")
	saveDialog.add_filter(saveDialogFilter)
	saveDialog.show()
	response = saveDialog.run()
	if response == gtk.RESPONSE_CANCEL:
		saveDialog.destroy()
	elif response == gtk.RESPONSE_OK:
		savedBackup = saveDialog.get_filename()
		saveDialog.destroy()
		splited = savedBackup.split(".")
		if len(splited) == 2:
			if splited[1].lower() != "ipb":
				savedBackup = savedBackup + ".ipb"
		else:
			savedBackup = savedBackup + ".ipb"
		#print savedBackup
		BackuPod_shared.MessageBox("Backup is about to start!","BackuPod is about to start backing up your iPod\nmusic library, this operation might take long time\ndepending on your iPod music library size.\nPlease don't disconnect your iPod during backup\noperation.")

		backup = zipfile.ZipFile(savedBackup,"w")
		backup._allowZip64 = True
		if podPath[len(podPath)-2:len(podPath)-1]:
			podPath += "/"
		filesIniPod = listiPodControl(podPath + "iPod_Control")
		sampleLib = file("library.lib", "w")
		sampleLib.write('<?xml version="1.0" ?>\n')
		sampleLib.write('<Music>\n')
		for fileToSave in filesIniPod:
			fileName = fileToSave.split(".")
			if len(fileName) == 2:
				
				if fileName[1] == "mp3":
					iPodPath = fileToSave[fileToSave.find("iPod_Control"):len(fileToSave)]
					sampleLib.write('\t<song name="%s">\n' % iPodPath)
					
					try:
						songInfo = EasyID3(fileToSave)
					except:
						songInfo = {"album":"UNKNOWN","artist":"UNKNOWN","title":"UNKNOWN","genre":"UNKNOWN","date":"UNKNOWN"}
					try:
						songINF = songInfo["album"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<album>%s</album>\n' % songINF)
					except:
						sampleLib.write('\t\t<album>UNKNOWN</album>\n')
					try:
						songINF = songInfo["artist"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<artist>%s</artist>\n' % songINF)
					except:
						sampleLib.write('\t\t<artist>UNKNOWN</artist>\n')
					try:
						songINF = songInfo["title"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<title>%s</title>\n' % songINF)
					except:
						sampleLib.write('\t\t<title>UNKNOWN</title>\n')
					try:
						songINF = songInfo["genre"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<genre>%s</genre>\n' % songINF)
					except:
						sampleLib.write('\t\t<genre>UNKNOWN</genre>\n')
					try:
						songINF = songInfo["date"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<year>%s</year>\n' % songINF)
					except:
						sampleLib.write('\t\t<year>UNKNOWN</year>\n')
					sampleLib.write('\t</song>\n')
				elif fileName[1] == "m4a" or fileName[1] == "m4b" or  fileName[1] == "mp4":
					iPodPath = fileToSave[fileToSave.find("iPod_Control"):len(fileToSave)]
					sampleLib.write('\t<song name="%s">\n' % iPodPath)
					
					songInfo = MP4(fileToSave)
					try:
						songINF = songInfo["\xa9alb"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<album>%s</album>\n' % songINF)
					except:
						sampleLib.write('\t\t<album>UNKNOWN</album>\n')
					try:
						songINF = songInfo["\xa9ART"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<artist>%s</artist>\n' % songINF)
					except:
						sampleLib.write('\t\t<artist>UNKNOWN</artist>\n')
					try:
						songINF = songInfo["\xa9nam"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<title>%s</title>\n' % songINF)
					except:
						sampleLib.write('\t\t<title>UNKNOWN</title>\n')
					try:
						songINF = songInfo["\xa9gen"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<genre>%s</genre>\n' % songINF)
					except:
						sampleLib.write('\t\t<genre>UNKNOWN</genre>\n')
					try:
						songINF = songInfo["\xa9day"][0].replace("&"," ")
						songINF = songINF.replace("<"," ")
						songINF = songINF.replace(">"," ")
						sampleLib.write('\t\t<year>%s</year>\n' % songINF)
					except:
						sampleLib.write('\t\t<year>UNKNOWN</year>\n')
					sampleLib.write('\t</song>\n')
		sampleLib.write('</Music>')
		del sampleLib
		backup.write("library.lib")
		print "Working....."
		for fileToSave in filesIniPod:
			backup.write(fileToSave)
		backup.close()
		print "Backup completed."
		self.wTree.get_widget("StatusBar").push(self.statusContext, "Backup completed.")
		BackuPod_shared.MessageBox("Backup Completed.","BackuPod finished backing up your iPod.\nBackup saved to: %s" % savedBackup)

def Backup(self):
	iPodPath = BackuPod_shared.getipodPath()
	if iPodPath != None:
		CreateBackup(self,iPodPath)