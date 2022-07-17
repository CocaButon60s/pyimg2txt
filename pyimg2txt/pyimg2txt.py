import tkinter as tk
import pyautogui as pag
import pyocr
from PIL import ImageEnhance
from .config import TESSDATA_PATH, TESSERACT_PATH
import os

class MainCanvas(tk.Canvas):
	def __init__(self, master:tk.Tk, width, height):
		super().__init__(master=master, width=width, height=height)
		self.bind('<ButtonPress-1>', self.press)
		self.bind('<Button1-Motion>', self.drawRect)
		self.bind('<ButtonRelease-1>', self.release)
		self.start_point = self.end_point = [0,0]
		self.pack() # キャンバスを表示する
	def drawRect(self, event):
		self.coords('rect1', self.start_point[0], self.start_point[1], event.x, event.y)
	def press(self, event):
		self.delete('rect1')
		self.create_rectangle(event.x,event.y,event.x,event.y,tag='rect1',fill='snow')
		self.start_point = [event.x, event.y]
	def release(self, event):
		self.end_point = [event.x,event.y]
		self.image2clipboard()
	def image2clipboard(self):
		global crop_image
		screenshot = pag.screenshot()
		crop_image = screenshot.crop(box=(self.start_point[0],self.start_point[1],self.end_point[0],self.end_point[1]))

class MainWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.attributes('-topmost', True) # tkinerウィンドウを常に最前面
		self.attributes('-fullscreen',True)
		self.attributes('-alpha',0.1)
		self.attributes('-transparentcolor','snow')
		self.bind('<Escape>', lambda event: self.destroy())
		self.bind('<ButtonRelease-1>', self.release)
		self.canvas = MainCanvas(self,self.winfo_screenwidth(),self.winfo_screenheight())
	def release(self, event):
		self.canvas.destroy()
		self.destroy()

def analyseImage():
	os.environ['PATH'] += os.pathsep + TESSERACT_PATH
	os.environ['TESSDATA_PREFIX'] = TESSDATA_PATH
	image = ImageEnhance.Contrast(crop_image.convert('L')).enhance(2.0)
	return pyocr.get_available_tools()[0].image_to_string(image,lang='jpn')

def getImageText():
	MainWindow().mainloop()
	return analyseImage()