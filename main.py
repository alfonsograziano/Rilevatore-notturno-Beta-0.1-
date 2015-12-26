import datetime,os
import pyaudio,wave
from sys import exit
from thread import start_new_thread
from Tkinter import *
from tkFileDialog import askdirectory
from time import sleep

def record():
    """
    questa funzione fa partire un file python che registra l'audio quando l'allarme scatta
    """

    conf = readFile("files/personalized.config")
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = sec.get()
    now = datetime.datetime.now()
    name = now.strftime("%Y-%m-%d %H:%M")
    WAVE_OUTPUT_FILENAME = os.path.join(pathname,name)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("record started in:  " + now.strftime("%Y-%m-%d %H:%M"))
    print("record terminate")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def controll():
    maxvolume = maxv.get()
    while x == 0:
        var = "rec -n stat trim 0 .01 2>&1 | awk '/^Maximum amplitude/' | cut -d" + ':' + " -f2 | sed 's/ //g'"
        p = os.popen(var,"r")
        volume = p.readline()
        volume = float(volume)*10
        if volume > 9:
            volume = 7.000
        print(volume)
        if volume > maxvolume:
            #parte il nuovo thread di registrazione
            start_new_thread(record, ())
            sleep(sec.get())

def start():
    global x
    x = 0
    start_new_thread(controll, ())
    lstate.config(text = "Stato programma: attivo")

def stop():
    global x
    x = 1
    lstate.config(text = "Stato programma: non attivo")

def browse():
    global pathname
    pathname = askdirectory(parent = root, title = "Select the folder...",)
    directory.config(text = "Salva in: " + pathname[:25] + "...")

def help():
    help_me = """
    This is a help guide of program
    ....
    ...

    """
    root = Tk()
    root.title("Help")
    root.resizable(False,False)
    root.config(bg = "white")
    l1 = Label(root, variable = help_me).pack()

def change():
    while True:
        var = "rec -n stat trim 0 .01 2>&1 | awk '/^Maximum amplitude/' | cut -d" + ':' + " -f2 | sed 's/ //g'"
        p = os.popen(var,"r")
        volume = p.readline()
        volume = float(volume)*10
        if volume > 9:
            volume = 9

        if volume < 2:
             lmic.config(image = mic0)
        elif volume < 3:
             lmic.config(image = mic1)
        elif volume < 4:
            lmic.config(image = mic2)
        elif volume < 6:
             lmic.config(image = mic3)
        elif volume < 7:
            lmic.config(image = mic4)
        elif volume < 8:
              lmic.config(image = mic5)
        elif volume < 9:
             lmic.config(image = mic6)
        elif volume == 9:
              lmic.config(image = mic7)

root = Tk()
root.title("Sensore notturno by lokk3d")
root.resizable(False,False)

menubar = Menu(root, bg = "white")

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0, bg = "white")
filemenu.add_command(label="Browse...", command=browse)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


helpmenu = Menu(menubar, tearoff=0, bg = "white")
helpmenu.add_command(label="About", command=help)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar, bg = "white")
moon = PhotoImage(file = "images/moon.gif")
lmoon = Label(root, image = moon, bg = "white")
istart = PhotoImage(file = "images/start.gif")
istop = PhotoImage(file = "images/stop.gif")
btstart = Button(root, image = istart, command = start)
btstop = Button(root, image = istop, command = stop)
lstate = Label(root, text = "Stato programma: non attivo", bg = "white")
separator = Frame(height=10, bd = 0, bg = "white", width = 20)
#set mic image
global mic0, mic1, mic2, mic3, mic4, mic5, mic6, mic7,lmic, sec
mic0 = PhotoImage(file = "images/mic0.gif")
mic1 = PhotoImage(file = "images/mic1.gif")
mic2 = PhotoImage(file = "images/mic2.gif")
mic3 = PhotoImage(file = "images/mic3.gif")
mic4 = PhotoImage(file = "images/mic4.gif")
mic5 = PhotoImage(file = "images/mic5.gif")
mic6 = PhotoImage(file = "images/mic6.gif")
mic7 = PhotoImage(file = "images/mic7.gif")
lmic = Label(root, image = mic0, bg = "white")
maxv = DoubleVar()
scale_bar = Scale(root, from_ = 0, to = 7, orient=HORIZONTAL, bg = "white",showvalue= 0,  variable = maxv)
sec = IntVar()
lsec = Label(root, text = "secondi di registrazione:", bg = "white")
sec_di = Spinbox(root, from_ = 0, to = 10000, bg = "white", textvariable = sec, width = 5)

start_new_thread(change, ())
#end of mic. part
directory = Label(root, text = "Salva in: ...", bg = "white")

#set all elements
lmoon.grid(row =0, column = 0,rowspan = 5,  columnspan = 2, padx = 5, pady = 5)
btstart.grid(row = 5, column = 0, padx = 5, pady = 5)
btstop.grid(row = 5, column = 1, padx = 5, pady = 5)
lstate.grid(row = 6, column = 0,columnspan = 2, padx = 5, pady = 5)
separator.grid(row =0, column = 2, padx = 5, pady = 5)
lmic.grid(row = 0,columnspan = 2, column = 3, padx = 15, pady = 15)
scale_bar.grid(row = 1, column = 3,columnspan = 2, padx = 15, pady = 15)
lsec.grid(row = 2, column = 3)
sec_di.grid(row = 2, column = 4, padx = 15, pady = 15)
directory.grid(row = 3, column = 3,columnspan = 2, padx = 15, pady = 15, sticky = W)
root.mainloop()
