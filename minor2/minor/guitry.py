from Tkinter import *
import tiny2_modified_5
import os
from PIL import ImageTk, Image
from tkFileDialog  import askopenfilename
#to import socket
import os, struct, socket

def close():
	    root.destroy()
while True:
	root = Tk()
	root.title("Proxy Cache Server")

	def callback():	
		tiny2_modified_5.main(E1.get(),int(E2.get()),E3.get())


	

	def fbrowse():
	    class App:
	    	def __init__(self, master):
			
			def bclose():
	    		    top.destroy()

			frame = Frame(master)
			frame.grid()

			self.button = Button(frame, text="QUIT", command=bclose)
			self.button.grid(row=2, ipadx=250)

			self.text = Text(frame)
			self.text.grid(row=0)

			self.choosen = askopenfilename(initialdir="/home/varsha/Desktop/CD/minor/")
			self.text.insert(END, open(self.choosen).read()) 
	       

	    top = Tk()
	    top.title("File Data")
	    app = App(top)
	    top.mainloop()

	def send():
	    # Take screenshot and load the data.
	    os.system('scrot image.jpg')
	    with open('image.jpg', 'rb') as file:
		data = file.read()
	    # Construct message with data size.
	    size = struct.pack('!I', len(data))
	    message = size + data
	    # Open up a server socket.
	    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    server.bind(('10.42.0.1', 45612))
	    server.listen(5)
	    # Constantly server incoming clients.
	    while True:
		client, address = server.accept()
		print('Sending data to:', address)
		# Send the data and shutdown properly.
		client.sendall(message)
		client.shutdown(socket.SHUT_RDWR)
		client.close()


	L1 = Label(root, text="IP address")
	L1.grid(row=0, column=0, pady=2, padx=6)
	E1 = Entry(root, bd =2)
	E1.grid(row=0, column=1, pady=2, padx=3)
	E1.insert(1, "127.0.0.2")

	L2= Label(root, text="Port")
	L2.grid(row=1, column=0, pady=2, padx=6)
	E2 = Entry(root, bd =2)
	E2.grid(row=1, column=1, pady=2, padx=3)
	E2.insert(1, "8000")

	L3= Label(root, text="Log")
	L3.grid(row=2,column=0, pady=2, padx=6)
	E3 = Entry(root, bd =2)
	E3.grid(row=2, column=1, pady=2, padx=3)
	E3.insert(1, "log.txt")
	B1 = Button(root, text="Start Server", command=callback)
	B1.grid(row=3, column=0, pady=5, padx=2)

	B1 = Button(root, text="Browse", command=fbrowse)
	B1.grid(row=3, column=1, padx=10, pady=5, ipadx=2, sticky=W)

	B1 = Button(root, text="send", command=send)
	B1.grid(row=3, column=1, pady=5, ipadx=5, sticky=E)

	B1 = Button(root, text="Exit", command=close)
	B1.grid(row=3, column=2, pady=10, ipadx=2, sticky=E)

	path = '/home/varsha/Desktop/CD/minor/proxy-org1.jpg'
	img = ImageTk.PhotoImage(Image.open(path))
	panel = Label(root, image = img)
	panel.grid(row=0, column=3, columnspan=2, rowspan=3,sticky=W+E+N+S, padx=5, pady=5)


	termf = Frame(root, height=200, width=700)
	termf.grid(row=4, column=0, columnspan=4)
	wid = termf.winfo_id()
	os.system('xterm -into %d -geometry 67x27 -sb -fn *-fixed-*-*-*-20-* &' % wid)

	root.protocol('WM_DELETE_WINDOW', close)
	root.mainloop()





	

	
	



