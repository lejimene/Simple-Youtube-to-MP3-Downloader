import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox 
from tkinter.font import Font
from pytube import YouTube
from collections import deque
import eyed3
import numpy as np
import eyed3
import os.path
from PIL import Image, ImageTk
import subprocess


class Mp3DownloaderApp:
    downloaded_videos = deque()
    
    def __init__(self, window):
        self.window = window
        self.window.title("MP3 Youtube Downloader")
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        self.window.minsize(600,500)
        
        self.TitleStr = tk.StringVar()
        self.AlbumnStr = tk.StringVar()
        self.ArtistStr = tk.StringVar()
        self.YearStr = tk.StringVar()
        self.LyricStr = tk.StringVar()
        self.ImagePath = tk.StringVar()
        self.GenreStr = tk.StringVar()
        self.DirPath = tk.StringVar()
        self.Volume = tk.StringVar()
        self.setup_ui()
                

    def setup_ui(self):
        window.columnconfigure((1, 2), weight=2)
        window.columnconfigure((0, 3), weight=2)
        window.rowconfigure((0, 3), weight=3)
        window.rowconfigure((1, 2, 4), weight=1)
        
        self.title_label = ttk.Label(self.window, text="Mp3 Upgrade", background="red", font=("Helvetica", 34))
        self.title_label.grid(row=0, column=1, columnspan=2, padx=10, sticky="nsew")

        self.user_str = tk.StringVar()
        self.entry = ttk.Entry(self.window, textvariable=self.user_str, font=("Helvetica", 10), background="white")
        self.entry.grid(row=1, column=1, columnspan=2, pady=10, sticky="ew")

        self.button_add = ttk.Button(self.window, text="Add", command=self.add_video)
        self.button_cfm = ttk.Button(self.window, text="Confirm", command=self.overlay_menu)
        self.button_add.grid(row=2, column=1, sticky="e", padx=8)
        self.button_cfm.grid(row=2, column=2, sticky="w", padx=8)

        self.listbox = tk.Listbox(self.window, background="pink")
        self.listbox.grid(row=3, column=1, columnspan=2, sticky="nsew", pady=20)
        self.listbox.bind("<Double-Button-1>", lambda event, lb=self.listbox: self.Double_Click(event, lb))
    
    def Double_Click(self, event, lb):
        index = lb.nearest(event.y)
        item = self.downloaded_videos[index]
        self.downloaded_videos.remove(item)
        self.update_listbox(lb)  
        
    def update_listbox(self,listbox):
        listbox.delete(0, tk.END)
        for key, _ in self.downloaded_videos:
            listbox.insert(tk.END, key)
        
    def clear_entry(self):
        self.entry.delete(0, 'end')
        return
        
    def add_video(self):
        self.duplicate_check()
        return
        
            
    def duplicate_check(self):
        url = self.user_str.get()
        video_title = self.get_video_title(url)
        if(self.universal_check() == False):
            return False
        else:
            if any(video[1] == url for video in self.downloaded_videos):
                self.clear_entry()
                messagebox.showinfo("Duplicate", "This Video is already in the Queue")
                return False
            else:
                self.downloaded_videos.append((video_title, url))
                self.listbox.insert(tk.END, video_title)
                self.clear_entry()
        return True
                
                
    def universal_check(self):
        url = self.user_str.get()
        
        if not url:
            messagebox.showinfo("Empty Link", "Provide a valid YouTube Link")
            return False

        if (self.valid_link(url) == False):
            messagebox.showwarning("Invalid URL", "Please provide a valid YouTube URL.")
            self.entry.delete(0, tk.END)  # Clear user_str entry
            return False
        
        return True
        
    def download(self):
        if not self.downloaded_videos:
            messagebox.showinfo("Queue Empty", "No videos in the queue to download.")
            return

        video_info = self.downloaded_videos[0]
        video_title, video_url = video_info

        try:
            yt = YouTube(video_url)
            audio_stream = yt.streams.get_by_itag(140)
            
            #FIX PATH NOT WORKING 
            if not (self.DirPath.get()):
                download_path = os.path.join(os.path.expanduser("~"), "Downloads")
            else:
                download_path = self.DirPath.get()
           
            
            if audio_stream:
                
                if not self.TitleStr.get():
                    video_title = (
                        video_title.replace('/', '-')
                                .replace('~', '')
                                .replace('{', '')
                                .replace('}', '')
                                .replace('[', '')
                                .replace(']', '')
                                .replace('"', '')  # Adding handling for quotation marks
                    )
                    # Replace the undesirable characters (including quotes) with an underscore
                    video_title = ''.join('_' if c in '/~{}[]" ' and c != ' ' else c for c in video_title)
                    base_filename = f"{video_title}.mp4"
                else:
                    title_str = self.TitleStr.get()
                    # Replace the undesirable characters (including quotes) with an underscore
                    title_str = ''.join(' ' if c in '/~{}[]" ' else c for c in title_str)
                    self.TitleStr.set(title_str)
                    base_filename = f"{title_str}.mp4"
                print(base_filename)
                full_path = os.path.join(download_path, base_filename)

                # Download the audio stream
                audio_stream.download(output_path=download_path, filename=base_filename)
                
                mp3_filename = os.path.splitext(full_path)[0] + ".mp3"
                if self.Volume.get():
                    db_value = float(self.Volume.get())
                    volume_factor = 10 ** (db_value / 10.0)  # Convert dB to linear factor
                    ffmpeg_cmd = f'ffmpeg -i "{full_path}" -vn -ar 44100 -ac 2 -ab 192k -af "volume={volume_factor}" -f mp3 "{mp3_filename}"'
                else:
                    ffmpeg_cmd = f'ffmpeg -i "{full_path}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{mp3_filename}"'
                subprocess.call(ffmpeg_cmd, shell=True)
                
                os.remove(full_path)
                
                audiofile = eyed3.load(mp3_filename)
                audiofile.initTag()
                audiofile.tag.artist = self.ArtistStr.get()
                audiofile.tag.album = self.AlbumnStr.get()
                audiofile.tag.title = self.TitleStr.get()
                audiofile.tag.year = self.YearStr.get()
                audiofile.tag.genre = self.GenreStr.get()
                if self.ImagePath.get():
                        artworkfile = open(self.ImagePath.get(),"rb")
                        artwork_data = artworkfile.read()
                        audiofile.tag.images.set(3, artwork_data, "image/jpeg", u"Front cover")
                        audiofile.tag.save(version=(2, 3, 0), filename=mp3_filename)
                audiofile.tag.save(version=(2,3,0))
            

                messagebox.showinfo("Download Complete", f"Downloaded '{video_title}' to {download_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading '{video_title}': {str(e)}")
        self.downloaded_videos.popleft()
        self.listbox.delete(0)
        self.restart()
        return

    def restart(self):
        #DONT RESTART DIRECTIONRY AND DIRECTORY OF PICTURE OF ALBUM
        self.AlbumnStr.set("")
        self.GenreStr.set("")
        if self.downloaded_videos:
            title_name = self.downloaded_videos[0][0]
            self.TitleStr.set(title_name)
        else:
            self.TitleStr.set("")
        self.YearStr.set("")
        self.Volume.set("")
        self.LyricStr.set("")
        self.ArtistStr.set("")
        return
        
        
        
    def cnf_check(self):
        url = self.user_str.get()
        video_title = self.get_video_title(url)
        if not (url):
            if not (self.downloaded_videos):
                messagebox.showwarning("Invalid URL", "Please provide a valid YouTube URL First.")
                return False #empty ENTRY AND EMPTY QUEUE
            else:
                return True # EMpty entry and FILLED QUEUE
            
        if not (self.valid_link(url)):
            messagebox.showwarning("Invalid URL", "Please provide a valid YouTube URL.")
            self.entry.delete(0, tk.END)  # Clear user_str entry 
            return False # NOT VALID ENTRY AND EMPTY QUEUE
            
        if (url) and not(self.downloaded_videos): #url is valid and nothing is inside queue
            self.downloaded_videos.append((video_title, url))
            self.listbox.insert(tk.END, video_title)
            self.clear_entry()
            return True
        
        if any(video[0] == video_title for video in self.downloaded_videos):
            self.clear_entry()
            messagebox.showinfo("Duplicate", "This Video is already in the Queue so was not added")
            return False
        else:
            self.downloaded_videos.append((video_title, url))
            self.listbox.insert(tk.END, video_title)
            self.clear_entry()
        return True



    def overlay_menu(self):
        
        if (self.cnf_check() == False):
             return
         
        # Hide main UI elements and show the overlay
        self.title_label.grid_forget()
        self.entry.grid_forget()
        self.button_add.grid_forget()
        self.button_cfm.grid_forget()
        self.listbox.grid_forget()
        self.show_overlay()
        return
        
    def open_image(self,event):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.pdf;*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff"),
                ("All files", "*.*")  # This allows all file types
            ]
        )
        self.ImagePath.set(file_path)
        self.show_image(event)
        return
    
    def show_image(self,event):
        image = Image.open(self.ImagePath.get())
        return
    
    def change_path(self):
        folder_path = filedialog.askdirectory()
        self.DirPath.set(folder_path)
        return
    
    def show_overlay(self):
        
        self.titleframe = ttk.Frame(self.window)
        self.leftmenu = ttk.Frame(self.window)
        self.middlemenu = ttk.Frame(self.window)
        self.rightmenu = ttk.Frame(self.window)
        
        self.titleframe.place(x=1, y=1 , relwidth = 1, relheight=.20)
        
        
        self.leftmenu.place(rely=.20,x=1,relwidth=.35,relheight=.80)
        

        self.middlemenu.place(relx=.35,rely=.20,relwidth=.35,relheight=.80)
        
        self.rightmenu.place(relx=.70,rely=.20,relwidth=.30,relheight=.80)
        
        if self.downloaded_videos:
            title_name = self.downloaded_videos[0][0]
            self.TitleStr.set(title_name)
            
        self.titleframe.rowconfigure(0,weight=1)
        self.titleframe.columnconfigure(0,weight=1)
        
        self.leftmenu.rowconfigure((0,2,4,6,8),weight=1)
        self.leftmenu.rowconfigure((1,3,5,7,9),weight=2)
        self.leftmenu.columnconfigure(0,weight=1)
        
        self.middlemenu.rowconfigure((0,3),weight=1)
        self.middlemenu.rowconfigure((1,2,4,5,6,7),weight=2)
        self.middlemenu.columnconfigure(0,weight=1)
        
        self.rightmenu.rowconfigure((0,2,3,4,5),weight=1)
        self.rightmenu.rowconfigure(1,weight=3)
        self.rightmenu.columnconfigure(0,weight=1)
        
        Maint = tk.Label(self.titleframe,text="Youtube Mp3 Downloader",font=("Helvetica 25"))
        Maint.grid(row=0,column=0,sticky="nwe",pady=5)
        
        title_label = tk.Label(self.leftmenu, text="Title", font=("Helvetica 15"))
        title_label.grid(row=0, column=0,padx=5, sticky="nw")

        title_entry = ttk.Entry(self.leftmenu, textvariable=self.TitleStr, font=("Helvetica 12"))
        title_entry.grid(row=1, column=0,padx=5,pady=2, sticky="nwe")


        artist_label = tk.Label(self.leftmenu, text="Artist", font=("Helvetica 15"))
        artist_label.grid(row=2, column=0, padx=5, sticky="nw")

        artist_entry = ttk.Entry(self.leftmenu, textvariable=self.ArtistStr, font=("Helvetica 12"))
        artist_entry.grid(row=3, column=0,pady=2,  padx=5, sticky="nwe")
        
        #2 , 0
        album_label = tk.Label(self.leftmenu, text="Albums", font=("Helvetica 15"))
        album_label.grid(row=4, column=0,  padx=5, sticky="nw")

        #3, 0 
        albumn_entry = ttk.Entry(self.leftmenu, textvariable=self.AlbumnStr, font=("Helvetica 12"))
        albumn_entry.grid(row=5, column=0, pady=2,  padx=5, sticky="nwe")

        year_label = tk.Label(self.leftmenu, text="Year", font=("Helvetica 15"))
        year_label.grid(row=6, column=0,  padx=5, sticky="nw")

        year_entry = ttk.Entry(self.leftmenu, textvariable=self.YearStr, font=("Helvetica 12"))
        year_entry.grid(row=7, column=0,pady=2,  padx=5, sticky="nwe")
        
        #ADD INT DEICBAL CHANGER
        
        genre_label = tk.Label(self.leftmenu,text="Genre",font=("Helvetica 15"))
        genre_label.grid(row=8,column=0,sticky="nw",padx=5)
        
        genre_entry = ttk.Entry(self.leftmenu,textvariable=self.GenreStr,font=("Helvetica 12"))
        genre_entry.grid(row=9,column=0,pady=5,padx=5,sticky="nwe")

        
        #MIDDLE 
        lyrics_label = tk.Label(self.middlemenu,text="Lyrics",font=("Helvetica 15"))
        lyrics_label.grid(row=0,column=0,padx=5,sticky="nswe")
        
        
        lyrics_text = tk.Text(self.middlemenu, font=("Helvetica 10"), width=1, height=5)
        lyrics_text.grid(row=1,rowspan=2,pady=5,column=0,sticky="nwse")  # Set rowspan to 4 for 4 rows

        Image_label = tk.Label(self.middlemenu,text="Album Cover",font=("Helvetica 15"))
        Image_label.grid(row=3,pady=5,sticky="nswe")
        
        Image_display = tk.Canvas(self.middlemenu, bg="black",width=1,height=5)
        Image_display.grid(row=4,rowspan=6,pady=8,sticky="nswe")
        Image_display.bind("<Button-1>", lambda event: self.open_image(event))
        
        #RIGHT
        listbox_label = tk.Label(self.rightmenu,text="Queue Left",font=("Helvetica 20"))
        listbox_label.grid(row=0,column=0,sticky="nwe",padx=5)
        
        self.listbox = tk.Listbox(self.rightmenu, background="lightblue")
        self.listbox.grid(row=1, column=0, sticky="wens", pady=5, padx=5)

        # Populate the new Listbox with items from downloaded_videos
        for video_info in self.downloaded_videos:
            self.listbox.insert(tk.END, video_info[0])
        

        change_dir = tk.Button(self.rightmenu,text="Change Directory",font=("Helvetica 15"),command=self.change_path)
        change_dir.grid(row=2,padx=5,column=0,pady=5,sticky="nsew")
        
        
        volume_label = tk.Label(self.rightmenu,text="Decibal Changer",font=("Helvetica 12"))
        volume_label.grid(row=3,padx=5,pady=5,sticky="nswe")
        
        volume_changer = tk.Entry(self.rightmenu,textvariable=self.Volume,font=("Helvetica 12"))
        volume_changer.grid(row=4,padx=5,pady=5,sticky="nswe")
        
        
        
        download_btn = tk.Button(self.rightmenu, text="Download", bg="pink", font=("Helvetica 20"), command=self.download)
        download_btn.grid(row=5, padx=5, column=0, pady=10, sticky="nswe")
        
        self.listbox.bind("<Double-Button-1>", lambda event, lb=self.listbox: self.Double_Click(event, lb))
        
        
        def check_downloaded_videos():
            if not self.downloaded_videos:
                self.titleframe.destroy()
                self.leftmenu.destroy()
                self.rightmenu.destroy()
                self.middlemenu.destroy()
                Maint.forget()
                title_label.forget()
                title_entry.forget()
                artist_entry.forget()
                artist_label.forget()
                album_label.forget()
                albumn_entry.forget()
                year_entry.forget()
                year_label.forget()
                genre_entry.forget()
                genre_label.forget()
                lyrics_label.forget()
                lyrics_text.forget()
                Image_label.forget()
                Image_display.forget()
                listbox_label.forget()
                self.listbox.forget()
                self.setup_ui()
                return True
            self.window.after(1000, check_downloaded_videos)
            
        if (check_downloaded_videos()):
            return
  
    
# width=15, height=15 
    def get_video_title(self, url):
        try:
            yt = YouTube(url)
            return yt.title
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    def valid_link(self, url):
        if "youtube.com" in url:
            return True
        return False

if __name__ == "__main__":
    window = tk.Tk()
    app = Mp3DownloaderApp(window)
    window.mainloop()
