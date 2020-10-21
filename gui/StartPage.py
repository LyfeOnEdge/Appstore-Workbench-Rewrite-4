import platform
from tkinter import ttk, Scrollbar, Frame, Text, Label, font
from .ResizableCanvas import ResizableCanvas
from fs.load_image import load_tk_image_from_bytes_array, load_image_object_from_bytes_array
from PIL import Image, ImageTk
from.AppPage import AppPage
class StartPage(ttk.Frame):
	def __init__(self, controller, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		self.controller = controller
		self.repos = []
		self.thumbnails = []
		self.tiles = []
		self.apppage = None

		canvas_container = Frame(self)
		canvas_container.pack(side = "top", fill = "both", expand = True)
		self.canvas_height = 720
		self.canvas_width = 1080
		self.canvas = ResizableCanvas(canvas_container, relief="sunken", background = "#333333")
		self.canvas.config(width = self.canvas_width, height = self.canvas_height, highlightthickness=0)
		self.scrollbar = Scrollbar(canvas_container)
		self.scrollbar.config(command=self.on_scroll_bar)      
		self.canvas.config(yscrollcommand=self.scrollbar.set) 
		self.scrollbar.pack(side="right", fill="y")
		self.canvas.pack(side = "right", expand=True, fill="both")
		self.canvas_frame = Frame(self.canvas, border = 0, highlightthickness = 0)
		self.canvas_frame.bind("<MouseWheel>", self._on_mouse_wheel)
		self.canvas_frame.config(width= self.canvas_width, height = self.canvas_height)
		self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')
		self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
		self.canvas.config(scrollregion=(0,0, self.canvas_height, self.canvas_height))
		# self.canvas.bind("<Enter>", self.mouse_enter)
		# self.canvas.bind("<Leave>", self.mouse_leave)
		self.canvas.bind("<Motion>", self.mouse_move)
		self.canvas.bind("<Button-1>", self.on_click)
		self.canvas.bind("<Configure>", self.on_configure)
		self.bind("<MouseWheel>", self._on_mouse_wheel)
		self.refresh()

	def on_configure(self, event = None):
		self.refresh()
		self.canvas.config(
			width=self.winfo_width(),
			height=self.winfo_height(),
			highlightthickness=0)

	# def mouse_enter(self, event): pass
	# def mouse_leave(self, event): pass
	
	def load_repo(self, repo):
		waiting_frame = Frame(self, background = "#333333")
		waiting_frame.place(relwidth = 1, relheight = 1)
		print(f"Loading repo {repo.name}")
		# waiting_text = Label(waiting_frame,
		# 	text = "Please wait while the repo loads...",
		# 	font = font.Font(size = 46, weight = "bold"),
		# 	background = "#333333",
		# 	foreground = "#CCCCCC",
		# )
		# waiting_text.place(
		# 	relwidth = 1,
		# 	relheight = 1
		# )
		waiting_text = Text(waiting_frame,
			wrap = "word",
			background = "#333333",
			foreground = "#CCCCCC",
			borderwidth = 0,
			highlightthickness = 0,
			font = font.Font(size = 46, weight = "bold"),
			)
		waiting_text.tag_configure("center", justify='center')
		waiting_text.insert("end", "Please wait while the repo loads")
		waiting_text.tag_add("center", "1.0", "end")
		waiting_text.configure(state = "disable")
		waiting_text.place(relwidth = 1, relheight = 1)
		
		def load_and_close_wait():
			repo.load_repo()
			self.apppage = AppPage(self.controller, repo, self)
			self.apppage.place(relwidth = 1, relheight = 1)
			waiting_frame.destroy()
			self.apppage.refresh()
			
		self.controller.threader.new_session()
		self.controller.threader.add(load_and_close_wait)

	def on_click(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_range(x,y):
				self.load_repo(t.repo)
			else: t.deactivate()

	def mouse_move(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_range(x,y):
				if t.active: continue
				else: t.activate()
			else: t.deactivate()

	def refresh(self, event = None):
		self.canvas.delete("all")
		self.thumbnails = []
		self.tiles = []
		self.canvas.delete("all")
		i = 0
		y_offset = 10
		y_padding = 50
		x_padding = 50
		tile_height = 200
		tile_width = 200
		framewidth = self.canvas.winfo_width() - self.scrollbar.winfo_width()
		self.canvas_frame.config(width=framewidth)
		# Get integer number of tiles fittable in the window
		maxperrow = framewidth // (tile_width + x_padding)
		#If there's not enough room to build anything stop
		if not maxperrow: return
		maxwidth = (maxperrow) * tile_width + maxperrow * x_padding
		filler_space = framewidth - maxwidth
		filler_space = filler_space / (maxperrow + 1)
		_x, _y = 0, 0 #vars to track where in grid we are placing
		for r in self.controller.repos:
			place_x = _x * tile_width + (_x + 1) * x_padding + (_x + 1) * filler_space
			place_y = _y * tile_height + y_offset + (_y + 1) * y_padding
			rt = Tile(self, r, load_image_object_from_bytes_array(r.image))
			self.tiles.append(rt)
			rt.set_dimensions(place_x,  place_y, tile_width, tile_height)
			self.place_tile(rt)
			_x += 1
			if _x == maxperrow: _x, _y = 0, _y + 1
		_y += 1
		height = _y * tile_height + y_offset + (_y + 1) * y_padding
		frameheight = self.canvas_frame.winfo_height()
		height = height if height > frameheight else frameheight
		self.canvas_height = height
		self.canvas_frame.config(width= 200, height = self.winfo_height())
		self.canvas.config(scrollregion=(0,0, 200, self.canvas_height))

	def place_tile(self, tile):
		tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height - 1, fill="#7F7F7F"))

		if tile.thumbnail:
			maxwidth = tile.width - 8
			maxheight = tile.width - 8
			art_image = tile.thumbnail
			wpercent = (maxwidth/float(art_image.size[0]))
			hsize = int((float(art_image.size[1])*float(wpercent)))
			new_image = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
			if new_image.size[1] >maxheight:
				hpercent = (maxheight/float(art_image.size[1]))
				wsize = int((float(art_image.size[0])*float(hpercent)))
				new_image = art_image.resize((wsize,maxheight), Image.ANTIALIAS)
			thumbnail = ImageTk.PhotoImage(new_image)

			self.thumbnails.append(thumbnail)
			tile.references.append(self.canvas.create_image(tile.x + 4, tile.y + 4, anchor = "nw", image = thumbnail))
		tile.references.extend([
			self.canvas.create_text(tile.x + 8, tile.y + 8, anchor = "nw", text = tile.repo_name, font = "bold", fill = "#CCCCCC")
		])
		if tile.active: self.activate_tile()
		
	def activate_tile(self, tile):
		tile.active_references.extend([
			self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width - 1, tile.y + tile.height - 1, outline="#000000", width = 4),
		])

	def deactivate_tile(self, tile):
		for r in tile.active_references:
			self.canvas.delete(r)

	def _on_mouse_wheel(self, event):
		if platform.system() == 'Windows':
			self.canvas.yview_scroll(-1 * int(event.delta / 120), 'units')
		elif platform.system() == 'Darwin':
			self.canvas.yview_scroll(-1 * int(event.delta), 'units')
		else:
			if event.num == 4:
				self.canvas.yview_scroll(-1, 'units')
			elif event.num == 5:
				self.canvas.yview_scroll(1, 'units')

	def on_scroll_bar(self, move_type, move_units, __ = None):
		if move_type == "moveto":
			self.canvas.yview("moveto", move_units)

	def exit(self, event = None):
		if self.apppage:
			try: self.apppage.exit()
			except: pass


class Tile:
	def __init__(self, manager, repo, thumbnail):
		self.x, self.y, self.width, self.height = None, None, None, None
		self.manager = manager
		self.thumbnail = thumbnail
		self.references = []
		self.active_references = []
		self.active = False
		self.repo_name = repo.name
		self.repo = repo

	def set_dimensions(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height

	def activate(self):
		self.active = True
		self.manager.activate_tile(self)

	def deactivate(self):
		self.active = False
		self.manager.deactivate_tile(self)

	def is_in_range(self, pointer_x, pointer_y):
		left_bound = self.x
		right_bound = self.x + self.width
		top_bound = self.y
		bottom_bound = self.y + self.height
		if pointer_x > left_bound and pointer_x < right_bound:
			if pointer_y > top_bound and pointer_y < bottom_bound:
				return True

	def on_click(self, pointer_x, pointer_y):
		return self.check_click_regions(pointer_x, pointer_y)

	def check_click_regions(self, pointer_x, pointer_y):
		def in_bounds(x, y, width, height):
			left_bound = x
			right_bound = x + width
			top_bound = y
			bottom_bound = y + height
			if pointer_x > left_bound and pointer_x < right_bound:
				if pointer_y > top_bound and pointer_y < bottom_bound:
					return True
		# def is_in_new_layer(): return in_bounds(self.new_x, self.new_y, 16, 16)
		# if is_in_new_layer(): self.manager.new_layer(self.frame); return True