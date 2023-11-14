from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from tkinter import messagebox
from ttkthemes import themed_tk as tk
import os


# Color values for dark mode
bg_dark = '#2E2E2E'
fg_dark = '#FFFFFF'
active_bg_dark = '#404040'
trough_color_dark = '#404040'

root = Tk()
root.title("MP3 Player")
root.geometry("600x400")
from tkinter import ttk
from tkinter import ttk

# For dark theme ---
# -------------------------------------------
# Create a style object
# style = ttk.Style()

# # Define a dark theme
# dark_theme = {
#     "TButton": {
#         "configure": {"background": "#2E2E2E", "foreground": "#FFFFFF"},
#         "map": {"background": [("active", "#404040")]}
#     },
#     "TEntry": {
#         "configure": {"background": "#2E2E2E", "foreground": "#FFFFFF"}
#     },
#     "TListbox": {
#         "configure": {"background": "#2E2E2E", "foreground": "#FFFFFF"},
#         "map": {"background": [("selected", "#404040")]}
#     },
#     "TScale": {
#         "configure": {"background": "#2E2E2E", "troughcolor": "#404040"}
#     },
# }

# # Set the theme to the dark theme
# style.theme_create("DarkTheme", parent="default", settings=dark_theme)
# style.theme_use("DarkTheme")



# Initialize Pygame Mixer
pygame.mixer.init()

# Grab Song Lenght time info
def play_time():
    # Check for double timing
    if stopped:
        return
    # grab current song time
    current_time = pygame.mixer.music.get_pos() / 1000

    # throe up temp label to get data
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song pos: {int(current_time)}')

    # convert to time format
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))

    # Get the current song (tuple number)

    current_song = song_box.curselection()
    # Grab song title srom playlist
    song = song_box.get(ACTIVE)

    # add directory strucute and mp3 to the playlist
    song = f'C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/{song}.mp3'

    
    # load Song  with mutagen
    song_mut = MP3(song)
    # Get song lenth
    global song_length
    song_length  = song_mut.info.length
    # convert to time format 
    converted_song_length= time.strftime('%M:%S',time.gmtime(song_length))

    # increse current time by 1sec
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length} ')

    elif paused:
        pass


    elif int(my_slider.get()) == int(current_time):
        # Update Slider To postion
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # Update Slider To postion
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        # convert to time format           
        converted_current_time = time.strftime('%M:%S',time.gmtime(int(my_slider.get())))

        # Output timt to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length} ')

        # Move this thing along by one second
        next_time = int(my_slider.get()) + 1

        my_slider.config(value=next_time)



    # # Output timt to status bar
    # status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length} ')

    # Update slider position vlaue to the current song
    # my_slider.config(value=int(current_time))


    # Update Time
    status_bar.after(1000, play_time)



# Add Song Function
def add_song():
    try:
        song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

        if not song:
            return  # User canceled file selection

        # Strip out the directory info and mp3 extension from the song name
        song = song.replace("C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/", "")
        song = song.replace(".mp3", "")

        # Add song to list box
        song_box.insert(END, song)

    except Exception as e:
        print(f"Error adding song: {e}")
        # Provide user feedback about the error, e.g., using a messagebox
        messagebox.showerror("Error", f"Error adding song: {e}")

# Add Many Songs to playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

    # Loop through song list and replace directory into and mp3
    for song in songs:

        # Strip out the directry info and mp3 extention from the song name
        song = song.replace("C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/", "")
        song = song.replace(".mp3", "")

        # Add song to list box
        song_box.insert(END, song)



# Play selected song
def play():
    try:
        # Set stop variabel to false so song can  play
        global stopped
        stopped = False
        song = song_box.get(ACTIVE)
        song = f'C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/{song}.mp3'

        # Play the Song
        pygame.mixer_music.load(song)
        pygame.mixer_music.play(loops=0)

        # Call the play_time function to get song lenght
        play_time()

        #  Update Slider To postion
        # slider_position = int(song_length)
        # my_slider.config(to=slider_position, value=0)


        current_volume = pygame.mixer_music.get_volume()
        # Times by 100 to make it easier to work with
        current_volume = current_volume * 100

        # change volume merter picure
        if int(current_volume) < 1:
            volume_meter.config(image=vol0)
        elif int(current_volume) > 0 and int(current_volume) <= 30:
            volume_meter.config(image=vol1)

        elif int(current_volume) > 30 and int(current_volume) <= 60:
            volume_meter.config(image=vol2)

        elif int(current_volume) > 60 and int(current_volume) <= 100:
            volume_meter.config(image=vol3)
    
    # if any error playing song this will thru error in message box
    except Exception as e:
        print(f"Error playing song: {e}")
        # Provide user feedback about the error, e.g., using a messagebox
        messagebox.showerror("Error", f"Error playing song: {e}")   

# Stop Playing current song
global stopped
stopped = False
def stop():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stop Song
    pygame.mixer_music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear the status bar
    status_bar.config(text='')

    # Set stop variable to true
    global stopped
    stopped = True
    
# Play The Next Song in the playlist
def next_song():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song (tuple number)
    next_one = song_box.curselection()
    # add one to the current song number
    next_one = next_one[0]+1
    # Grab song title srom playlist
    song = song_box.get(next_one)

    # add directory strucute and mp3 to the playlist
    song = f'C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/{song}.mp3'

    # Play the Song
    pygame.mixer_music.load(song)
    pygame.mixer_music.play(loops=0)

    # Clear active bar in playlist
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Set active bar to next song
    song_box.selection_set(next_one, last=None)

# Play previous song in playlist
def previous_song():
    # Reset Slider and Status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    
    # Get the current song (tuple number)
    next_one = song_box.curselection()
    # add one to the current song number
    next_one = next_one[0]-1
    # Grab song title srom playlist
    song = song_box.get(next_one)

    # add directory strucute and mp3 to the playlist
    song = f'C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/{song}.mp3'

    # Play the Song
    pygame.mixer_music.load(song)
    pygame.mixer_music.play(loops=0)

    # Clear active bar in playlist
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Set active bar to next song
    song_box.selection_set(next_one, last=None)

# Delete a song
def delete_song():
    stop()
    # Delete Currently Selected Song
    song_box.delete(ANCHOR)
    # Stop music if it's playing
    pygame.mixer_music.stop()

# Delete all songs
def delete_all_songs():
    stop()
    song_box.delete(0, END)
    # Stop music if it's playing
    pygame.mixer_music.stop()



# Create Global Pause variable
global paused
paused = False


# Pause and Unpause The Current Song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:   
        # Unpause
        pygame.mixer_music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer_music.pause()
        paused = True

# Create slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')

    song = song_box.get(ACTIVE)
    song = f'C:/Users/Dell/OneDrive/Desktop/python.py/tkinter/audio/{song}.mp3'

    # Play the Song
    pygame.mixer_music.load(song)
    pygame.mixer_music.play(loops=0, start=int(my_slider.get()))

# Create volume function
def volume(x):
    pygame.mixer_music.set_volume(volume_slider.get())
    
    current_volume = pygame.mixer_music.get_volume()
    # Times by 100 to make it easier to work with
    current_volume = current_volume * 100

    # change volume merter picure
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)

    elif int(current_volume) > 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)

    elif int(current_volume) > 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)

    elif int(current_volume) > 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)
    



# create master frame
master_frame = Frame(root)
master_frame.pack()

# Create Playlist Box
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

# Define Player control buttons images
back_btn_img = PhotoImage(file="backward1.png")
forward_btn_img = PhotoImage(file="forward1.png")
play_btn_img = PhotoImage(file="play1.png")
pause_btn_img = PhotoImage(file="pause1.png")
stop_btn_img = PhotoImage(file="stop1.png")

# Define Volume Control Images
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file="novolume.png")
vol1 = PhotoImage(file="volume1.png")
vol2 = PhotoImage(file="volume2.png")
vol3 = PhotoImage(file="volume3.png")
vol4 = PhotoImage(file="volume4.png")



# Create Player control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# Create volume meter 
volume_meter = Label(master_frame, image=vol3)
volume_meter.grid(row=1, column=1, padx=10)

# create volume frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)

# Create Player control buttons
back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_btn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

# Grid the all buttons
back_btn.grid(row=0, column=0, padx=10)
forward_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Add Many Songs to the Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_song)

# create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

# Create Volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)


# Create Temporary Slider Label
# slider_label = Label(root, text="0")
# slider_label.pack(pady=10)

# Create a menu for theme switching
# theme_menu = Menu(my_menu)
# my_menu.add_cascade(label="Theme", menu=theme_menu)
# theme_menu.add_command(label="Toggle Theme", command=toggle_theme)

root.mainloop()