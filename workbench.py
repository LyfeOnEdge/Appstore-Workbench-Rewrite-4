import os, json, threading, traceback
from tkinter import ttk, Tk, Toplevel, Listbox, Button, StringVar, Frame, messagebox
from PIL import Image, ImageTk
from appstore import Appstore
from gui.RootWindow import RootWindow
from fs.load_image import load_tk_image_from_bytes_array
from threader.Threader import Threader
DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH = 150
HEIGHT = 250
OFFSET = 5

# tkinter.Tk.report_callback_exception

cache_folder = os.path.join(DIR, "cache")
if not os.path.isdir(cache_folder): os.mkdir(cache_folder)
json_folder = os.path.join(cache_folder, "json")
if not os.path.isdir(json_folder): os.mkdir(json_folder)

class Controller:
	def __init__(self, devmode = False):
		self.devmode = devmode
		self.canvases = []
		self.version = "4 Alpha 1"
		self.repos = []
		self.threader = Threader(30)
		
	def start_mainloop(self):
		self.load_repos()
		self.root = RootWindow(self)
		self.root.mainloop()

	def load_repos(self):
		with open(os.path.join(DIR, "repos.json")) as rf:
			repos = json.loads(rf.read())
			for r in repos:
				self.repos.append(
					Appstore(
						r["name"],
						r["path"],
						image = r["image"].encode("latin1")
					)
				)

	def report_callback_exception(self, *args):
		messagebox.showerror('Exception', traceback.format_exception(*args))

if __name__ == "__main__":
	app = Controller(devmode = True)
	app.start_mainloop() #Call tk mainloop