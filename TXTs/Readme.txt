Prerequisites:
Python:
	https://www.python.org/downloads/
Pip:
	py -m ensurepip --upgrade
	Download the script, from https://bootstrap.pypa.io/get-pip.py	
	Open a terminal/command prompt, cd to the folder containing the get-pip.py file and run:
	py get-pip.py

Cmake:
	https://cmake.org/download/
	! add to path aktivieren !

Pip packages:
	OpenCV:
		pip install opencv-python (alternativ: pip3 install opencv-python)
	Pygame:
		pip install pygame
	dlib: (wahrscheinlich nicht mehr benötigt, da durch Mediapipe ersetzt)
		pip install dlib
		evtl. muss dafür dafür Visual Studio für C++ installiert
	mediapipe:
		pip install mediapipe
		(wenn andere Python Versionen installiert: Versuche: C:\Users\DEINEN_NAME_HIER_EINFÜGEN\AppData\Local\Programs\Python\Python311/python -m pip install mediapipe)
		Für mediapipe: Python Interpreter auf 3.11 einstellen (Strg + Shift + P -> Python: Select Interpreter)
		und Mediapipe für 3.11 installieren
	pyrealsense2:
		Pfad/zur/Installation/Python311/python.exe -m pip install pyrealsense2

Python Tipps:
Wenn mehrere Python Versionen installiert sind und eine bestimmte Version genutzt werde soll, so kann man vor die Python-
Befehle den Pfad des Python Interpreters setzten, z.B. C:\Users\Jonas\AppData\Local\Programs\Python\Python311\python.exe
Diesen findet man, wenn man im Windows Start-Menü "Python 3.11" eingibt und dann den Dateipfad der .exe öffnet
