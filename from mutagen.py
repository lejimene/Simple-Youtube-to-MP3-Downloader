from pytube import YouTube
import os
import subprocess
import eyed3
from pytube import Search
import requests
import tkinter as tk
from tkinter import filedialog

# Replace 'video_url' with the URL of the YouTube video you want to download
video_url = 'https://www.youtube.com/watch?v=kHKDuAJ5Po8'
s = Search('Ultra Sounds ye Unreleased')
len(s.results)
print(s.results)

# Create a YouTube object
yt = YouTube(video_url)

    
# Get the highest quality audio stream
audio_stream = yt.streams.get_by_itag(140)
download_path = os.path.join(os.path.expanduser("~"), "Downloads")
base_filename = f"Kanye West - Flowers [DONDA 2] [NEW LEAK].mp4"
full_path = os.path.join(download_path, base_filename)

# Download the audio stream
audio_stream.download(output_path=download_path, filename=base_filename)

# Use FFmpeg to convert the file to MP3 format
mp3_filename = os.path.splitext(full_path)[0] + ".mp3"
ffmpeg_cmd = f'ffmpeg -i "{full_path}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{mp3_filename}"'
subprocess.call(ffmpeg_cmd, shell=True)

os.remove(full_path)
# Initialize and add ID3 tags using eyed3


# Delete the original MP4 file


print(f"Converted and saved as: {mp3_filename}")



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

def add_album_artwork():
    audiofile = eyed3.load(mp3_filename)
    
    # Specify the path to your album artwork image file
    artwork_file_path = open_file_dialog()
    print(artwork_file_path)

    artworkfile = open(artwork_file_path,"rb")
    artwork_data = artworkfile.read()
    audiofile.tag.images.set(3, artwork_data,"Image files", "Front cover")
    audiofile.tag.save(version=(2, 3, 0), filename=mp3_filename)
    
    # Embed the album artwork
    #if artwork_file_path:
    #    with open(artwork_file_path, "rb") as artwork_file:
    #        artwork_data = artwork_file.read()
    #        audiofile.tag.artist = "Kanye West"
    #        audiofile.tag.title = "Flowers [DONDA 2] [NEW LEAK]"
    #        audiofile.tag.album = "DONDA 2"
    #        audiofile.tag.images.set(3, artwork_data,"Image files", "Front cover")
    #        audiofile.tag.save(version=(2, 3, 0), filename=mp3_filename)

root = tk.Tk()
root.title("File Selection")

button = tk.Button(root, text="Open File Dialog", command=add_album_artwork)
button.pack()

root.mainloop()



