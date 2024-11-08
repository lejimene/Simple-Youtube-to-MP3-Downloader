import tkinter as tk
from tkinter import ttk

class YourApplication:
    def __init__(self, window):
        self.window = window
        self.window.title("Your Application")
        self.window.geometry('600x500')
        self.window.minsize(600,500)


        self.TitleStr = tk.StringVar()
        self.AlbumnStr = tk.StringVar()
        self.ArtistStr = tk.StringVar()
        self.YearStr = tk.StringVar()
        self.GenreStr =tk.StringVar()
        
        titleframe = ttk.Frame(self.window)
        leftmenu = ttk.Frame(self.window)
        middlemenu = ttk.Frame(self.window)
        rightmenu = ttk.Frame(self.window)
        
        titleframe.place(x=1, y=1 , relwidth = 1, relheight=.20)
        
        
        leftmenu.place(rely=.20,x=1,relwidth=.35,relheight=.80)
        

        middlemenu.place(relx=.35,rely=.20,relwidth=.35,relheight=.80)
        
        
        
        rightmenu.place(relx=.70,rely=.20,relwidth=.30,relheight=.80)
        

        titleframe.rowconfigure(0,weight=1)
        titleframe.columnconfigure(0,weight=1)
        
        leftmenu.rowconfigure((0,2,4,6,8),weight=1)
        leftmenu.rowconfigure((1,3,5,7,9),weight=2)
        leftmenu.columnconfigure(0,weight=1)
        
        middlemenu.rowconfigure((0,3),weight=1)
        middlemenu.rowconfigure((1,2,4,5,6,7),weight=2)
        middlemenu.columnconfigure(0,weight=1)
        
        rightmenu.rowconfigure((0,2,3),weight=1)
        rightmenu.rowconfigure(1,weight=3)
        rightmenu.columnconfigure(0,weight=1)
        
        Maint = tk.Label(titleframe,text="Youtube Mp3 Downloader",font=("Helvetica 25"))
        Maint.grid(row=0,column=0,sticky="nwe",pady=5)
        
        title_label = tk.Label(leftmenu, text="Title", font=("Helvetica 15"))
        title_label.grid(row=0, column=0,padx=5, sticky="nw")

        title_entry = ttk.Entry(leftmenu, textvariable=self.TitleStr, font=("Helvetica 12"))
        title_entry.grid(row=1, column=0,padx=5,pady=2, sticky="nwe")

        album_label = tk.Label(leftmenu, text="Albums", font=("Helvetica 15"))
        album_label.grid(row=2, column=0,  padx=5, sticky="nw")

        albumn_entry = ttk.Entry(leftmenu, textvariable=self.AlbumnStr, font=("Helvetica 12"))
        albumn_entry.grid(row=3, column=0, pady=2,  padx=5, sticky="nwe")

        artist_label = tk.Label(leftmenu, text="Artist", font=("Helvetica 15"))
        artist_label.grid(row=4, column=0, padx=5, sticky="nw")

        artist_entry = ttk.Entry(leftmenu, textvariable=self.ArtistStr, font=("Helvetica 12"))
        artist_entry.grid(row=5, column=0,pady=2,  padx=5, sticky="nwe")

        year_label = tk.Label(leftmenu, text="Year", font=("Helvetica 15"))
        year_label.grid(row=6, column=0,  padx=5, sticky="nw")

        year_entry = ttk.Entry(leftmenu, textvariable=self.YearStr, font=("Helvetica 12"))
        year_entry.grid(row=7, column=0,pady=2,  padx=5, sticky="nwe")
        
        #BRAND NEW ADD THIS
        
        genre_label = tk.Label(leftmenu,text="Genre",font=("Helvetica 15"))
        genre_label.grid(row=8,column=0,sticky="nw",padx=5)
        
        genre_entry = ttk.Entry(leftmenu,textvariable=self.GenreStr,font=("Helvetica 12"))
        genre_entry.grid(row=9,column=0,pady=5,padx=5,sticky="nwe")

        
        #MIDDLE 
        lyrics_label = tk.Label(middlemenu,text="Lyrics",font=("Helvetica 15"))
        lyrics_label.grid(row=0,column=0,padx=5,sticky="nswe")
        
        
        lyrics_text = tk.Text(middlemenu, font=("Helvetica 10"), width=1, height=5)
        lyrics_text.grid(row=1,rowspan=2,pady=5,column=0,sticky="nwse")  # Set rowspan to 4 for 4 rows

        Image_label = tk.Label(middlemenu,text="Album Cover",font=("Helvetica 15"))
        Image_label.grid(row=3,pady=5,sticky="nswe")
        
        Image_display = tk.Canvas(middlemenu, bg="black",width=1,height=5)
        Image_display.grid(row=4,rowspan=6,pady=8,sticky="nswe")
        Image_display.bind("<Button-1>")
        

        listbox_label = tk.Label(rightmenu,text="Queue Left",font=("Helvetica 20"))
        listbox_label.grid(row=0,column=0,sticky="swe",padx=5)
        
        self.listbox = tk.Listbox(rightmenu)
        self.listbox.grid(row=1, column=0, sticky="wens", pady=5, padx=5)
        
        change_dir = tk.Button(rightmenu,text="Change Directory",font=("Helvetica 15"))
        change_dir.grid(row=2,padx=5,column=0,pady=5,sticky="nsew")
        
        download_btn = tk.Button(rightmenu, text="Download", bg="pink", font=("Helvetica 20"), command=self.download)
        download_btn.grid(row=3, padx=5, column=0, pady=10, sticky="nswe")
        
        # ...
        
# ...


    def download(self):
        # Implement your download logic here
        pass

def main():
    root = tk.Tk()
    app = YourApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
