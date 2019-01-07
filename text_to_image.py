import binascii
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
import PIL.Image
import numpy as np

def encode():
    st = myEntryBox.get()
    st = st.replace('\n', ' ')
    st = st.strip()
    bin_string = bin(int.from_bytes(st.encode(), 'big'))
    bin_string = bin_string[2:]
    #bin_string = '0' + bin_string

    bin_array = np.array(list(bin_string))
    sz = bin_array.size
    barr_dim_size = int(np.ceil(np.sqrt(sz)))

    padding = np.zeros((barr_dim_size**2-sz,), dtype=int)
    bin_array = np.concatenate((bin_array,padding))

    bin_array = np.reshape(bin_array,(barr_dim_size,barr_dim_size))

    bin_array = bin_array.astype(int)
    bin_array *= 255

    img = PIL.Image.fromarray(bin_array)
    width, height = img.size
    maxsize = 700
    factor = maxsize/width
    width = int(width*factor)
    height = int(height*factor)

    img = img.resize((width, height))
    image = ImageTk.PhotoImage(img)
    canvas.image = image
    if width > maxsize:
        canvas.config(width=width, height=height)
    else:
        canvas.config(width=maxsize, height=maxsize)
    canvas.create_image(width, height, image = image, anchor = SE)
    
#
## Convert image back into text
#bitarr = np.asarray(img, dtype=np.uint8)
#bits = bitarr.ravel()
#bits = bits//255
#bits = np.trim_zeros(bits, 'b')
#bits = bits.tolist()
#str1 = ''.join(str(e) for e in bits)
#
#new_padding_len = int(((np.ceil(len(str1)/8)-1)*8+7)-sz)
##print(int(np.ceil(len(str1)/8)))
#str1 = '0b' + str1 + new_padding_len*'0'
#
#n = int(str1, 2)
#aaa = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
#print(aaa)



interface = Tk()
interface.title("Text-Binary Image Converter")
frame = Frame(interface)

L1 = Label(frame, text="Text to encode:")
L1.grid(column=1,row=1,sticky=E)

def openfile():
    return filedialog.askopenfilename()

def savefile():
    return filedialog.asksaveasfilename()

myEntryBox = ttk.Entry(frame)
myEntryBox.grid(column=2,row=1,sticky=W)

button = ttk.Button(frame, text="Encode", command=encode)
button.grid(column=1,row=2,sticky=E)

button = ttk.Button(frame, text="Open", command=openfile)
button.grid(column=2,row=2,sticky=W)

canvas = Canvas(frame, width=330, height=330, bg="white")
canvas.grid(column=1,row=3,columnspan=2)
canvas.image = None

button = ttk.Button(frame, text="Save image", command=savefile)
button.grid(column=1,row=4,columnspan=2)

for child in interface.winfo_children(): child.grid_configure(padx=0, pady=0)

interface.mainloop()