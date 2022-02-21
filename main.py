# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import eel

from FileManager import askOpenFileName


eel.init('web')


@eel.expose
def create_file():
	path = askOpenFileName()

	return path


if __name__ == '__main__':
	eel.start('index.html')