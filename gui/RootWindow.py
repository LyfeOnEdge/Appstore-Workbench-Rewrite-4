from tkinter import ttk, messagebox
from .StartPage import StartPage

class RootWindow(ttk.Frame):
	def __init__(self, controller):
		ttk.Frame.__init__(self)
		#Controller to allow inter-window access, passed to all windows
		self.controller = controller 
		#Because we are instantiating a widget without passing it a parent one is created for the ttk.Frame
		#This is some trickery that allows a tk.Toplevel to be in control of the tkinter mainloop without
		#establishing a proper tk.Root
		#Because the tk.toplevel was instantiated behind the scenes we have to grab it
		self.window = self._nametowidget(self.winfo_parent()) #Get toplevel window name
		self.window.bind("<Escape>", self.exit) #Bind escape key to exit window
		self.window.title(f"Appstore-Workbench Version {controller.version}") #Set window title
		self.window.geometry("1080x720") #Set window start size
		#Override normal exit protocol when the close button is pushed to shut down gently instead
		self.window.protocol("WM_DELETE_WINDOW", self.exit)

		if self.controller.devmode:
			self.window.report_callback_exception = self.controller.report_callback_exception


		#Place self (ttk.Frame) to fill window
		self.startpage = StartPage(controller, self)
		self.startpage.place(relwidth = 1, relheight = 1)

		self.place(relwidth = 1, relheight = 1)

	def exit(self, *args):
		if messagebox.askyesno("Exit?", "Are you sure you wish to exit?"):
			self.startpage.exit()
			self.window.destroy()
			self.controller.threader.exit()
