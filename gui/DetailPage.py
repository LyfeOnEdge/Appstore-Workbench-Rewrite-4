import os
from PIL import Image, ImageTk
from tkinter import Frame, font, Text, Label
from fs.load_image import load_tk_image_from_bytes_array, load_image_object_from_bytes_array

back_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x002\x00\x00\x002\x08\x06\x00\x00\x00\x1e?\x88\xb1\x00\x00\x01\x84iCCPICC Profile\x00\x00x\x9c}\x91=H\xc3@\x1c\xc5_[\xa5R*\x0ef\x10\xe9\x90\xa1:Y\x11\x15q\x94*\x16\xc1Bi+\xb4\xea`r\xe9\x174iHR\\\x1c\x05\xd7\x82\x83\x1f\x8bU\x07\x17g]\x1d\\\x05A\xf0\x03\xc4\xc9\xd1I\xd1EJ\xfc_Rh\x11\xe3\xc1q?\xde\xdd{\xdc\xbd\x03\xfc\xcd*S\xcd\x9e\t@\xd5,#\x9d\x88\x8b\xb9\xfc\xaa\x18|E\x08\x02\x02\x18GDb\xa6\x9e\xcc,f\xe19\xbe\xee\xe1\xe3\xeb]\x8cgy\x9f\xfbs\xf4+\x05\x93\x01>\x91x\x8e\xe9\x86E\xbcA<\xb3i\xe9\x9c\xf7\x89\x05V\x96\x14\xe2s\xe21\x83.H\xfc\xc8u\xd9\xe57\xce%\x87\xfd<S0\xb2\xe9yb\x81X,u\xb1\xdc\xc5\xacl\xa8\xc4\xd3\xc4QE\xd5(\xdf\x9fsY\xe1\xbc\xc5Y\xad\xd6Y\xfb\x9e\xfc\x85\xe1\x82\xb6\x92\xe1:\xcd\x08\x12XB\x12)\x88\x90QG\x05UX\x88\xd1\xaa\x91b"M\xfbq\x0f\xff\xb0\xe3O\x91K&W\x05\x8c\x1c\x0b\xa8A\x85\xe4\xf8\xc1\xff\xe0w\xb7fqj\xd2M\n\xc7\x81\xde\x17\xdb\xfe\x18\x01\x82\xbb@\xaba\xdb\xdf\xc7\xb6\xdd:\x01\x02\xcf\xc0\x95\xd6\xf1\xd7\x9a\xc0\xec\'\xe9\x8d\x8e\x16=\x02\x06\xb6\x81\x8b\xeb\x8e&\xef\x01\x97;\xc0\xd0\x93.\x19\x92#\x05h\xfa\x8bE\xe0\xfd\x8c\xbe)\x0f\x0c\xde\x02\xa15\xb7\xb7\xf6>N\x1f\x80,u\xb5|\x03\x1c\x1c\x02\xa3%\xca^\xf7xw_wo\xff\x9ei\xf7\xf7\x03\x95\x9fr\xb5o|U\x0b\x00\x00\x00\xf0IDATx\x9c\xed\x99K\x16\x840\x08\x04{\xe6\xfeW\xf69\xab\xec\xd4\x97\x00\xdd`\x86\xda\xfa-\t\tD\xa0i\x9a\xe6M|\x92\x9e{F\xbf\x83Z\xe4|8\xe6z\x97\xaf\xe7\xe2E\x9e$\xdc\xa8Df$\\\xa2\n\x11j$\x06l\x11\x89\x04\xc0\x15Y\x95(\x99\xec\xb2H\x0c\x18"\x16\t\xf72\x10-\x92"\x01\xc4\x8a\xa4I\x00q"\xa9\x12@\x8cH\xba\x040/rw\xdeax&\xa5\xbe\xf3\xdc\xb4D$\x06\xd6\xa1UJ\x02\xd0\x15\x8d\xf4v\xc1""-=faGD\xd6\xb8\xfdu\xf5\xbb\xfa\x95\xb7\xe8G\x06t\x19\xab\x88e\xec\x97\xed\xd9\xb3\xb6\x92.\xf1\x0e\xad2\xf9\x12\x91#%d\xa2\x92=]&r\xd6J\x95\x89\x9e~\xd3d\x94[\xa6w\x84\xc80DR\xd6\x18VD\xe4k\x0cshI\xf3\xa5\xcb\xf8\x05\xb6h\xac\x0632%7\xb1\xaf\xa0Ff\x9b\x9f\xa1M\xd34\xef\xe2\x07K\xdd\x1fI\x87\xc6\xc3\x9c\x00\x00\x00\x00IEND\xaeB`\x82'


buttonsize = 20
image_fraction = 0.4
offset = 5
title_height = 20
columnwidth = 200
class DetailPage(Frame):
	def __init__(self, controller, repo, package, *args, **kwargs):
		Frame.__init__(self,*args,**kwargs)
		self.controller = controller
		self.package = package
		self.repo = repo
		self.bind("<Configure>", self.on_configure)
		self.updating = False

		self.back_image = load_image_object_from_bytes_array(back_image)
		self.back_button = ImageTk.PhotoImage(self.back_image)


		self.body = Frame(self, background ="#333333")
		self.body.place(relwidth = 1, relheight = 1, width = - columnwidth)

		self.image_frame = Frame(self.body, background ="#333333")
		self.image_frame.place(relwidth=1, relheight = image_fraction)

		self.banner_image = Label(self.image_frame, background ="#333333")
		self.banner_image.place(relwidth = 1, relheight = 1)

		backlabel = Label(self.image_frame, image = self.back_button, background ="#333333")
		backlabel.place(x = 10, y = 10)
		backlabel.bind("<Button-1>", self.exit)

		self.details = Text(self.body, font = font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
		
		self.details.place(relwidth = 1,
			relheight = 1 - image_fraction,
			rely = image_fraction,
			x = 2 * offset,
			width = - 4 * offset,
			y = + 2 * offset,
			height = -4 * offset,
		)

		def construct():

			#RIGHT COLUMN
			self.column = Frame(self, background ="#333333")
			self.column.place(relx = 1, rely = 0, width = columnwidth, relheight = 1, x = - columnwidth)

			self.column_body = Frame(self.column, background ="#333333")
			self.column_body.place(relwidth=1, relheight=1)

			self.column_title = Label(self.column_body, anchor="w", font=font.Font(size = 10, weight = "bold"), background ="#333333", foreground = "#CCCCCC")
			self.column_author = Label(self.column_body, anchor="w", font=font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
			self.column_version = Label(self.column_body, anchor="w", font=font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
			self.column_license = Label(self.column_body, anchor="w", font=font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
			self.column_package = Label(self.column_body, anchor="w", font=font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
			self.column_downloads = Label(self.column_body, anchor="w", font=font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
			self.column_updated = Label(self.column_body, anchor="w", font=font.Font(size = 10), background ="#333333", foreground = "#CCCCCC")
			column_labels = [self.column_title, self.column_author, self.column_version, self.column_license, self.column_package, self.column_downloads, self.column_updated]
			for l in column_labels:
				l.pack(side = "top", padx = 4, pady = (0,4), fill = "x", expand = False)

			self.column_title.configure(text = "Title: {}".format(package["title"]))
			self.column_author.configure(text = "Author: {}".format(package["author"]))
			self.column_version.configure(text = "Latest Version: {}".format(package["version"]))
			try: self.column_license.configure(text = "License: {}".format(package["license"]))
			except: self.column_license.configure(text = "License: N/A")
			self.column_package.configure(text = "Package: {}".format(package["name"]))

			ttl_dl = 0
			try: ttl_dl += package["web_dls"]
			except: pass
			try: ttl_dl += package["app_dls"]
			except: pass

			self.column_downloads.configure(text = "Downloads: {}".format(ttl_dl))
			self.column_updated.configure(text = "Updated: {}".format(package["updated"]))
			self.details.configure(state = "normal")
			self.details.delete(0.0,"end")
			self.details.insert("end", package["details"].replace("\\n", """
	"""))
			self.details.configure(state = "disable")

		self.controller.threader.do(construct)



# 		self.update_buttons(package)

# 	def update_buttons(self, package):
# 		#Hides or places the uninstalll button if not installed or installed respectively
# 		#get_package_entry returns none if no package is found or if the sd path is not set
# 		if self.appstore_handler.get_package_entry(package["name"]):
# 			self.column_uninstall_button.place(rely=1,relwidth = 1, x = + 2 * offset, y = - 1 * (buttonsize + offset), width = - (4 * offset + buttonsize), height = buttonsize)
# 			if self.column_install_button:
# 				if self.appstore_handler.clean_version(self.appstore_handler.get_package_version(package["name"]), package["title"]) > self.appstore_handler.clean_version(package["version"], package["title"]):
# 					self.column_install_button.settext("UPDATE")
# 				else:
# 					self.column_install_button.settext("REINSTALL")
# 		else:
# 			self.column_uninstall_button.place_forget()
# 			if self.column_install_button:
# 				self.column_install_button.settext("INSTALL")

# 	def select_version(self, option):
# 		try:
# 			self.selected_version = option
# 			self.version_index = self.controller.appstore_handler.get_tag_index(self.package["github_content"], self.selected_version)
# 			self.update_release_notes()
# 		except Exception as e:
# 			# print(e)
# 			pass

	def on_configure(self, event=None): self.update_banner()

	def update_banner(self):
		bannerimage = self.repo.getScreenImage(self.package["name"])
		if bannerimage: self.controller.threader.do(self.do_update_banner, [bannerimage])
		else: self.controller.threader.do(self.do_update_banner, ["gui/assets/notfound.png"])

	#only call this on a separate thread or it will block the main loop
	def do_update_banner(self,image_path):
		if self.updating: return
		self.updating = True
		self.banner_image.image = None
		while True:
			maxheight = self.image_frame.winfo_height()
			maxwidth = self.image_frame.winfo_width()
			if maxwidth > 3 and maxheight > 3:
				art_image = Image.open(image_path)
				wpercent = (maxwidth/float(art_image.size[0]))
				hsize = int((float(art_image.size[1])*float(wpercent)))
				if hsize <= 3: continue
				new_image = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
				if new_image.size[1] > maxheight:
					hpercent = (maxheight/float(art_image.size[1]))
					wsize = int((float(art_image.size[0])*float(hpercent)))
					if hsize <= 3: continue
					new_image = art_image.resize((wsize,maxheight), Image.ANTIALIAS)
				art_image = ImageTk.PhotoImage(new_image)
				self.banner_image.configure(image=art_image)
				self.banner_image.image = art_image
				break
		self.updating = False

# 	def show(self, package, handler):
# 		self.showing = True
# 		self.appstore_handler = handler
# 		self.package_parser = handler
# 		self.do_update_banner("gui/assets/notfound.png")
# 		threader.do_async(self.update_page, [package], priority = "medium")
# 		self.tkraise()
# 		for child in self.winfo_children():
# 			child.bind("<Escape>", self.leave)

	def exit(self, event = None):
		print("Destroying")
		self.destroy()

# 	def reload_function(self):
# 		print("Reloading")
# 		self.app.load_plugin(self.package.get("binary"))
# 		self.app.reload_category_frames()
# 		self.reload()

# 	def trigger_install(self):
# 		if not self.appstore_handler.check_path():
# 			self.set_sd()
# 		if self.appstore_handler.check_path():
# 			if self.appstore_handler.check_if_get_init():
# 				if self.package:
# 					threader.do_async(self.appstore_handler.handler_install_package, [self.package, self.progress_bar.update, self.reload_function, self.progress_bar.set_title], priority = "high")
# 			else:
# 				self.yesnoPage.getanswer("The homebrew appstore has not been initiated here yet, would you like to initiate it?", self.init_get_then_continue)

# 	def init_get_then_continue(self):
# 		self.appstore_handler.init_get()
# 		self.trigger_install()

# 	def trigger_uninstall(self):
# 		if self.package:
# 			self.appstore_handler.uninstall_package(self.package)
# 			self.app.reload_category_frames(True)
# 			self.app.after(100, self.reload)

# 	def reload(self):
# 		threader.do_async(self.update_page, [self.package])

# 	def trigger_open_tab(self):
# 		if self.package:
# 			try:
# 				url = self.package["url"]
# 				opentab(url)
# 			except Exception as e:
# 				print("Failed to open tab - {}".format(e))

# 	def set_sd(self):
# 		chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
# 		self.appstore_handler.set_path(chosensdpath)
# 		self.reload()