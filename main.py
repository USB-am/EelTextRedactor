# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import eel


eel.init('web')


@eel.expose
def create_file():
	path = 'PATH'

	return path


if __name__ == '__main__':
	eel.start('index.html')