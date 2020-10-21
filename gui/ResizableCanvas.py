from tkinter import Canvas
# a subclass of Canvas for dealing with resizing of windows
class ResizableCanvas(Canvas):
	def __init__(self,parent,**kwargs):
		Canvas.__init__(self,parent,**kwargs)
		self.configure(borderwidth = 0, highlightthickness = 0)
		self.bind("<Configure>", self.on_resize)
		self.height = self.winfo_reqheight()
		self.width = self.winfo_reqwidth()

	def resize(self, oldwidth, oldheight, newwidth, newheight):
		wscale = newwidth/oldwidth
		hscale = newheight/oldheight
		self.config(width=newwidth, height=newheight)
		self.scale("all",0,0,wscale,hscale)
		self.width = newwidth
		self.height = newheight

	def on_resize(self,event):
		self.resize(self.width, self.height,event.width, event.height)
	def refresh(self):
		self.resize(self.width, self.height, self.winfo_reqwidth(), self.winfo_reqheight())