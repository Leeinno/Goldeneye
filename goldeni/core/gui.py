#!/usr/bin/python

import Tkinter
import Image,ImageTk,tkFileDialog,sys,tkMessageBox,cv
import main

import main

class mainWindow(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent=parent
		self.initialize()

	def changePara(self):
		cpara = Tkinter.Toplevel(bg="white")
		cpara.title("Advanced Configuration Options")
		cpara.geometry('250x250+0+0')

		#### Use arrays ####
		L1 = Tkinter.Label(cpara, text="Hamming Distance: ",bg="white")
		L1.pack()
		E1 = Tkinter.Entry(cpara, bd=2)
		E1.pack()

		L2 = Tkinter.Label(cpara, text="Median Filter Radius: ",bg="white")
		L2.pack()
		E2 = Tkinter.Entry(cpara, bd=2)
		E2.pack()

		L3 = Tkinter.Label(cpara, text="Hough Transform Option",bg="white")
		L3.pack()
		E3 = Tkinter.Entry(cpara, bd=2)
		E3.pack()

		L2 = Tkinter.Label(cpara, text="Unspecified Parameter",bg="white")
		L2.pack()
		E2 = Tkinter.Entry(cpara, bd=2)
		E2.pack()
		###################
		

        	button = Tkinter.Button(cpara, text="Submit", command=self.paraSubmit)
       		button.pack(side = Tkinter.BOTTOM)

	def queryDatabase(self):
		query = Tkinter.Toplevel(bg="white")
		query.title("Input IrisCode")
		query.geometry('250x250+0+0')

	def aboutProj(self):
		aproj = Tkinter.Toplevel(bg="white")
		aproj.title("Project Goldeneye")
		aproj.geometry('250x250+0+0')

		message = "Project Members: \nMatt, Joe, Ricky\n\nDetails:\n"
		Tkinter.Label(aproj,text=message,bg="white").pack()

	def loadImage(self):
		imgPath = tkFileDialog.askopenfilename(filetypes=[("all files","*"),("images","*.py")])
		loadImage = ImageTk.PhotoImage(file=imgPath)

		self.background.destroy()
		self.b1.destroy()
		self.b2.destroy()

		self.title("Iris Processing")

		self.newimage = Tkinter.Label(self, image=loadImage)
		self.newimage.loadImage=loadImage
		self.newimage.grid(row=0,column=0,rowspan=2,columnspan=2)

		self.button = Tkinter.Button(self, text="Process Image",command=lambda i=imgPath: self.processImage(i) ,bg="white")
		self.button.grid(row=2,column=0,columnspan=2)

	def paraSubmit(self):
		tkMessageBox.showinfo("Iris Processing", "Test")

	def searchRecord(self):
		tkMessageBox.showinfo("SEARCHING...", "RECORD")

	def processImage(self,path):
		self.newimage.destroy()
		self.title("Iris Processed")
		self.button.destroy()

		loadImage = ImageTk.PhotoImage(main.main(path))
		self.newimage = Tkinter.Label(self, image=loadImage)
		self.newimage.loadImage=loadImage
		self.newimage.grid(row=0,column=0,rowspan=2,columnspan=2)
		
		self.button = Tkinter.Button(self, text="Close",command=self.quit ,bg="white")
		self.button.grid(row=2,column=0,columnspan=2)

	def initialize(self):
		self.grid()

		self.backImage = ImageTk.PhotoImage(file="images/1.gif")
		self.background = Tkinter.Label(self,image=self.backImage,bg="black")
		self.background.grid(row=0,column=0,columnspan=2,rowspan=2)

		self.grid_columnconfigure(0,weight=1)
		#self.resizable(True,False)

		menubar=Tkinter.Menu(self)
		filemenu = Tkinter.Menu(menubar,tearoff=0)
		filemenu.add_command(label="Change Parameters",command=self.changePara)
		filemenu.add_separator()
		filemenu.add_command(label="Quit",command=self.quit)

		menubar.add_cascade(label="File",menu=filemenu)

		helpmenu = Tkinter.Menu(menubar,tearoff=0)
		helpmenu.add_command(label="About Project",command=self.aboutProj)
		menubar.add_cascade(label="Help",menu=helpmenu)

		self.config(menu=menubar)

		self.b1 = Tkinter.Button(self, text="Load Image", command=self.loadImage,bg="white")
		self.b1.grid(row=3,column=0)

		self.b2 = Tkinter.Button(self, text="Search for Record", command=self.searchRecord,bg="white")
		self.b2.grid(row=3,column=1)


if __name__ == "__main__":
	root = mainWindow(None)
	root.title("Healthcare Iris Biometric Scanner")
	root.mainloop()

