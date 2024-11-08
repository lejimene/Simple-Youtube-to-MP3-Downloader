import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageTk



def show_full_image(event):
	global resized_tk

	# current ratio 
	canvas_ratio = event.width / event.height

	# get coordinates 
	if canvas_ratio > image_ratio: # canvas is wider than the image
		height = int(event.height)
		width = int(height * image_ratio) 
	else: # canvas is narrower than the image
		width = int(event.width) 
		height = int(width / image_ratio)



	resized_image = image_original.resize((width, height))
	resized_tk = ImageTk.PhotoImage(resized_image)
	canvas.create_image(
		int(event.width / 2),
		int(event.height / 2),
		anchor = 'center',
		image = resized_tk)
 
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.pdf;*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff"),
            ("All files", "*.*")  # This allows all file types
        ]
    )
    if file_path:
        # Do something with the selected file path
        print("Selected file:", file_path)
        return file_path
# exercise:
# create a third scaling behaviour to always show the full image without cutting off parts

# setup
window = tk.Tk()
window.geometry('600x400')
window.title('Images')

# grid layout
window.columnconfigure((0,1,2,3), weight = 1, uniform = 'a')
window.rowconfigure(0, weight = 1)

# import an image 
image_original = Image.open(open_file_dialog())
image_ratio = image_original.size[0] / image_original.size[1]
print(image_ratio)
image_tk = ImageTk.PhotoImage(image_original)


# widget
# label = ttk.Label(window, text = 'raccoon', image = image_tk)
# label.pack()



# canvas -> image
canvas = tk.Canvas(window, background = 'white', bd = 0, highlightthickness = 0, relief = 'ridge')
canvas.grid(column = 1, columnspan = 3, row = 0, sticky = 'nsew')

canvas.bind('<Configure>', show_full_image)

# run
window.mainloop()