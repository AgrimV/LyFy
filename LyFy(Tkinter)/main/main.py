"""
Script to display the
lyrics to the user
"""
import tkinter as tk
import platform
import lyfy
import os

ROOT = tk.Tk()
CURRENT_SONG = ''
LYR = ''


def refresh():
    """
    Refresh the lyric window
    """
    global CURRENT_SONG
    if not lyfy.get_spotify_song_data()['title'] == CURRENT_SONG:
        frame()
    else:
        pass


def save():
    """
    Save the current lyrics
    to $HOME/saved
    """
    global LYR
    name = lyfy.get_spotify_song_data()['title']
    if platform.system() == 'Linux':
        home = os.environ['HOME']
        os.system('mkdir $HOME/saved')
        with open(home + '/saved/' + name + '.txt', 'w') as file:
            file.write(LYR)
    else:
        os.system('mkdir ./saved')
        with open('./saved/' + name, 'w') as file:
            file.write(LYR)



def frame():
    """
    Frame to display the lyrics
    """
    global ROOT, CURRENT_SONG, LYR
    root = tk.Tk()
    root.title("LyFy")
    CURRENT_SONG = lyfy.get_spotify_song_data()['title']
    if 'Linux' in platform.system():
        root.iconbitmap('@./icon/lyrics.xbm')
    else:
        root.iconbitmap('@./icon/lyrics.ico')
    root.geometry("400x600")
    btn1 = tk.Button(root, text="Reload", command=refresh)
    btn1.pack(pady=10)
    btn2 = tk.Button(root, text="Save", command=save)
    btn2.pack()
    scrollbar = tk.Scrollbar(root)
    listbox = tk.Listbox(root, yscrollcommand=scrollbar.set,
                         height=500, width=45)
    LYR = lyfy.print_lyrics()
    for line in LYR.split("\n"):
        listbox.insert(tk.END, line)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    ROOT.destroy()
    ROOT = root
    listbox.pack(pady=15)
    root.mainloop()


frame()
