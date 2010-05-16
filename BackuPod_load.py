import gtk
import zipfile

from xml.dom import minidom

def loadBackupFile(self):
	loadDialog = gtk.FileChooserDialog("Load Backup File", self.wTree.get_widget("BackuPodForm"), gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	loadDialogFilter = gtk.FileFilter()
	loadDialogFilter.set_name("iPod Backup File")
	loadDialogFilter.add_pattern("*.ipb")
	loadDialog.add_filter(loadDialogFilter)
	loadDialog.show()
	response = loadDialog.run()
	if response == gtk.RESPONSE_CANCEL:
		loadDialog.destroy()
	elif response == gtk.RESPONSE_OK:
		backupFileName = loadDialog.get_filename()
		loadDialog.destroy()
		backupFile = zipfile.ZipFile(backupFileName, 'r')
		backupFile_allowZip64 = True
		i= 1
		# songs list
		songsListStore = gtk.ListStore(str,str,str,str,str)
		if self.wTree.get_widget("lstSongs").get_model() != None:
			ColumnToDelete0 = self.wTree.get_widget("lstSongs").get_column(0)
			ColumnToDelete1 = self.wTree.get_widget("lstSongs").get_column(1)
			ColumnToDelete2 = self.wTree.get_widget("lstSongs").get_column(2)
			ColumnToDelete3 = self.wTree.get_widget("lstSongs").get_column(3)
			ColumnToDelete4 = self.wTree.get_widget("lstSongs").get_column(4)
			self.wTree.get_widget("lstSongs").remove_column(ColumnToDelete0)
			self.wTree.get_widget("lstSongs").remove_column(ColumnToDelete1)
			self.wTree.get_widget("lstSongs").remove_column(ColumnToDelete2)
			self.wTree.get_widget("lstSongs").remove_column(ColumnToDelete3)
			self.wTree.get_widget("lstSongs").remove_column(ColumnToDelete4)
		albumColumn = gtk.TreeViewColumn('Album')
		artistColumn = gtk.TreeViewColumn('Artist')
		titleColumn = gtk.TreeViewColumn('Title')
		genreColumn = gtk.TreeViewColumn('Genre')
		yearColumn = gtk.TreeViewColumn('Date')
		self.wTree.get_widget("lstSongs").set_model(songsListStore)
		
		# add songs to songs list
		for fileIn in backupFile.namelist():
			#print fileIn
			if fileIn.rfind("/") != -1:
				tmpLibFile = fileIn[fileIn.rfind("/")+1:len(fileIn)]
			else:
				tmpLibFile = fileIn
			if tmpLibFile == "library.lib":
				libFile = minidom.parseString(backupFile.read(fileIn))
				songsNodes = []
				for node in libFile.firstChild.childNodes:
					#if node.nodeName.encode("ascii") == "song":
					if node.nodeName == "song":
						songsNodes.append(node)
				for item in songsNodes:
					albumInfo = item.getElementsByTagName("album")[0].firstChild.data
					artistInfo = item.getElementsByTagName("artist")[0].firstChild.data
					titleInfo = item.getElementsByTagName("title")[0].firstChild.data
					genreInfo = item.getElementsByTagName("genre")[0].firstChild.data
					yearInfo = item.getElementsByTagName("year")[0].firstChild.data
					songsListStore.append((albumInfo,artistInfo,titleInfo,genreInfo,yearInfo))
		
		albumColumn.set_sort_column_id(0)
		#albumColumn.set_expand(True)
		artistColumn.set_sort_column_id(1)
		#artistColumn.set_expand(True)
		titleColumn.set_sort_column_id(2)
		#titleColumn.set_expand(True)
		genreColumn.set_sort_column_id(3)
		#genreColumn.set_expand(True)
		yearColumn.set_sort_column_id(4)
		#yearColumn.set_expand(True)
		
		self.wTree.get_widget("lstSongs").append_column(albumColumn)
		self.wTree.get_widget("lstSongs").append_column(artistColumn)
		self.wTree.get_widget("lstSongs").append_column(titleColumn)
		self.wTree.get_widget("lstSongs").append_column(genreColumn)
		self.wTree.get_widget("lstSongs").append_column(yearColumn)
		
		cell = gtk.CellRendererText()
		albumColumn.pack_start(cell, True)
		albumColumn.set_attributes(cell, text=0)
		artistColumn.pack_start(cell, True)
		artistColumn.set_attributes(cell, text=1)
		titleColumn.pack_start(cell, True)
		titleColumn.set_attributes(cell, text=2)
		genreColumn.pack_start(cell, True)
		genreColumn.set_attributes(cell, text=3)
		yearColumn.pack_start(cell, True)
		yearColumn.set_attributes(cell, text=4)
		
		self.wTree.get_widget("StatusBar").push(self.statusContext, "Backup Loaded.")
		
	loadDialog.destroy()