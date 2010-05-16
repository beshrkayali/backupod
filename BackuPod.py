#!/usr/bin/env python2.5
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#----------------------------------------------
# BackuPod | Backup your iPod music | version 2.0
# Created by Beshr Kayali | Beshrkayali@gmail.com
# http://BackuPod.sourceforge.net
# Started at:    08:05 PM		1/17/2008
# Finished at:   11:13 AM		1/20/2008
#----------------------------------------------
import gtk.glade
import sys
import pango, atk, cairo, pangocairo
import encodings

#BackuPod additionals
import BackuPod_shared
import BackuPod_load
import BackuPod_backup
import BackuPod_restore

class BackuPod_Main:
	def __init__(self):
		self.wTree = gtk.glade.XML("backupod.glade", "BackuPodForm")
		dic={
		#Quit Button
		"on_BackuPodForm_destroy" : self.quit,
		"on_btnQuit_clicked" : self.quit,
		"on_mnuFileQuit_activate" : self.quit,
		#About Dialog
		"on_mnuHelpAbout_activate" : self.about,
		"on_btnAbout_clicked" : self.about,
		#Load Backup
		"on_btnLoadBackup_clicked" : self.loadBackup,
		"on_mnuFileLoadBackupFile_activate" : self.loadBackup,
		#Do Backup
		"on_btnBackupiPod_clicked" : self.DoBackup,
		"on_mnuToolsCreateBackupFile_activate" : self.DoBackup,
		#Do Restore
		"on_btnRestoreiPod_clicked" :self.DoRestore,
		"on_mnuToolsRestoretoiPod_activate" : self.DoRestore,

		}
		self.wTree.signal_autoconnect (dic)
		
		#status bar
		self.statusContext = self.wTree.get_widget("StatusBar").get_context_id("BackuPod StatusBar")
		self.wTree.get_widget("BackuPodForm").set_icon_from_file("sIcon.png")
		self.wTree.get_widget("StatusBar").push(self.statusContext, "Ready.")
	def quit(self,obj):
		"Handles the quiting."
		gtk.main_quit()
		sys.exit(1)
	def about(self,obj):
		BackuPod_shared.showAbout()
	def loadBackup(self,obj):
		BackuPod_load.loadBackupFile(self)
	def DoBackup(self,obj):
		BackuPod_backup.Backup(self)
	def DoRestore(self,obj):
		BackuPod_restore.Restore(self)

if __name__ == '__main__':
	BackuPod_Main()
	try:
        	gtk.gdk.threads_init()
	except:
		print "BackuPod 2.0 can't run without threading enabled in your pyGTK!"
		sys.exit(1)
		
	gtk.gdk.threads_enter()
	gtk.main()
	gtk.gdk.threads_leave()
