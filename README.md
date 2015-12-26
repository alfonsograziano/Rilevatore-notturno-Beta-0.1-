# Rilevatore-notturno-Beta-0.1-
This a simple python software. 
It use "Tkinter" library for GUI and "pyaudio" for record.
This program use a third part software, that run from terminal. 
This is the string code of the third part program: "rec -n stat trim 0 .01 2>&1 | awk '/^Maximum amplitude/' | cut -d" + ':' + " -f2 | sed 's/ //g'"

