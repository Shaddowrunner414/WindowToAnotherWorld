Prerequisites:
Python:
	https://www.python.org/downloads/
Pip:
	py -m ensurepip --upgrade
	Download the script, from https://bootstrap.pypa.io/get-pip.py	
	Open a terminal/command prompt, cd to the folder containing the get-pip.py file and run:
	py get-pip.py

Pip packages:
	OpenCV:
		pip install opencv-python (alternativ: pip3 install opencv-python)
	Pygame:
		pip install pygame
	mediapipe:
		pip install mediapipe
	pyrealsense2:
		pip instsall pyrealsense2
	
Die packages sollten schon installiert sein. Entweder als Abhängigkeit der oberen oder sind in der Python Installtion standardmäßig enthalten
	Systemmodule:
		pip install sys
		pip install os
	Numpy:	
		pip install numpy
	


Tipp:
Wenn mehrere Python Versionen installiert sind und eine bestimmte Version genutzt werde soll, so kann man vor die Python-
Befehle den Pfad des Python Interpreters setzten, z.B. C:\Users\Jonas\AppData\Local\Programs\Python\Python311\python.exe
Diesen findet man, wenn man im Windows Start-Menü "Python 3.11" eingibt und dann den Dateipfad der .exe öffnet
Für pip Installationen also: Pfad/zur/Installation/Python311/python.exe -m pip install


Zum Bauen der exe:
pip install pyinstaller
pyinstaller WindowToAnotherWorld.spec  