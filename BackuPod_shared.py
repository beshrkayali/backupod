import os
import gtk


def MessageBox(Message,Secondary):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,Message)
	dialog.format_secondary_text(Secondary)
	dialog.run()
	dialog.destroy()

def getAnswer(Message,Secondary):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,Message)
	dialog.format_secondary_text(Secondary)
	respond = dialog.run()
	return respond,dialog

def showAbout():
	aboutDialog = gtk.AboutDialog()
	aboutDialog.set_name("BackuPod")
	aboutDialog.set_version("2.0")
	aboutDialog.set_comments("Backup your iPod music")
	aboutDialog.set_copyright("\302\251 2008 Beshr Kayali")
	aboutDialog.set_website("http://backupod.sourceforge.net/")
	aboutDialog.set_license("""BackuPod is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

BackuPod is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.""")
	aboutDialog.set_wrap_license(True)
	aboutDialog.set_icon_from_file("Main.png")
	aboutDialog.set_logo(aboutDialog.get_icon())
	aboutDialog.connect ("response", lambda d, r: d.destroy())
	aboutDialog.show()

def getipodPath():
	available_disks = ("A:\\","B:\\","C:\\","D:\\","E:\\","F:\\","G:\\","H:\\","I:\\","J:\\","K:\\","L:\\","M:\\","N:\\","O:\\","P:\\","Q:\\","R:\\","S:\\","T:\\","U:\\","V:\\","W:\\","X:\\","Y:\\","Z:\\")
	for disk_name in available_disks:
		if os.path.exists("%siPod_Control"  % disk_name) == True:
			return disk_name
			MessageBox("iPod found!","Connected iPod was found in "+disk_name)
	if disk_name != None:
		dialog = gtk.Dialog("Couldn't find your iPod path", None, 0,(gtk.STOCK_OK, gtk.RESPONSE_OK,"Cancel", gtk.RESPONSE_CANCEL))
		hbox = gtk.HBox(False, 8)
		hbox.set_border_width(8)
		dialog.vbox.pack_start(hbox, False, False, 0)
		stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION,gtk.ICON_SIZE_DIALOG)
		hbox.pack_start(stock, False, False, 0)
		
		table = gtk.Table(2, 2)
		table.set_row_spacings(4)
		table.set_col_spacings(4)
		hbox.pack_start(table, True, True, 0)

		label = gtk.Label("iPod Path:")
		label.set_use_underline(True)
		table.attach(label, 0, 1, 0, 1)
		local_entry1 = gtk.Entry()
		table.attach(local_entry1, 1, 2, 0, 1)
		label.set_mnemonic_widget(local_entry1)

		label = gtk.Label('Like: "H:/"')
		label.set_use_underline(True)
		table.attach(label, 0, 2, 1, 2)

		dialog.show_all()
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			if os.path.exists(local_entry1.get_text() + "/iPod_Control/"):
				dialog.destroy()
				return local_entry1.get_text()
			else:
				dialog.destroy()
				MessageBox("iPod not found!","The path you've entered is not an iPod.\nPlease connect an iPod and try again.")
	dialog.destroy()