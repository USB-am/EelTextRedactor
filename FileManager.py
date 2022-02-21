# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
from datetime import datetime


class FolderElement:
	def __init__(self, path: str, name: str):
		self.path = path
		self.name = name
		self.absolute_path = os.path.join(self.path, self.name)

	def get_attrs(self) -> tuple:
		result = (self.name, self.__get_date(), self.__get_type())

		return result

	def __get_date(self) -> str:
		last_change_unix_time = os.path.getmtime(self.absolute_path)
		date = datetime.fromtimestamp(last_change_unix_time)
		result = date.strftime('%d.%m.%Y %H:%M:%S')

		return result

	def __get_type(self) -> str:
		if self.is_file():
			ext = os.path.splitext(self.name)[1]
			if ext:
				return f'Файл "{ext.upper()}"'
			else:
				return 'Файл'
		else:
			return 'Папка с файлами'

	def is_file(self):
		return os.path.isfile(self.absolute_path)


def get_elements_from_folder(path: str) -> tuple:
	result = (FolderElement(path, name) for name in os.listdir(path))

	return result


def sorted_folder_elements(elements_attrs: tuple) -> tuple:
	result = sorted(elements_attrs,
		key=lambda element: (element[2], element[0])
	)
	return result


def get_elements_attrs(elements: tuple[FolderElement]) -> tuple:
	result = (element.get_attrs() for element in elements)

	return result


def get_folder_elements_attrs(path: str) -> tuple:
	elements = get_elements_from_folder(path)
	elements_attrs = get_elements_attrs(elements)
	sorted_elements = sorted_folder_elements(elements_attrs)

	return sorted_elements


class FolderTreeview(tk.Frame):
	HEADINGS_NAMES = ('Name', 'Date', 'Type')

	def __init__(self, parent: tk.Frame, **options):
		super().__init__(parent)

		self.treeview = ttk.Treeview(self, show='headings',
			columns=FolderTreeview.HEADINGS_NAMES, **options)

		for heading in FolderTreeview.HEADINGS_NAMES:
			self.treeview.heading(heading, text=heading)

		# self.treeview.bind('<<TreeviewSelect>>', self.selected)

		scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
		self.treeview.config(yscroll=scroll_y.set)

		self.treeview.grid(row=0, column=0)
		scroll_y.grid(row=0, column=1, sticky=tk.NS)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

	def selected(self, event: tk.Event) -> None:
		for selection in self.treeview.selection():
			item = self.treeview.item(selection)
			name = item['values'][0]

	def insertElements(self, path: str) -> None:
		elements = get_folder_elements_attrs(path)

		for element in elements:
			self.treeview.insert('', tk.END, values=element)

	def clear(self) -> None:
		self.treeview.delete(*self.treeview.get_children())

	def item(self, item: str) -> dict:
		return self.treeview.item(item)

	def selection(self) -> tuple:
		return self.treeview.selection()


class UI(tk.Frame):
	def __init__(self, parent: tk.Tk, now_folder: str):
		super().__init__(parent)

		self.global_path = tk.StringVar()
		self.global_path.set(now_folder)
		self.__create_ui()

	def __create_ui(self) -> None:
		# ===== TOP PANEL ===== #
		top_panel = tk.Frame(self)
		top_panel.pack(side='top', fill='x')

		self.back_btn = tk.Button(top_panel, text='←')
		self.back_btn.pack(side='left', padx=(10, 5), pady=5)
		# back_btn.bind('<Button-1>', lambda e: print('Back button'))

		self.global_path_entry = ttk.Entry(top_panel, textvariable=self.global_path)
		self.global_path_entry.pack(side='left', fill='x', expand=tk.ON,
			padx=(5, 17), pady=10)
		# global_path_entry.bind('<Return>', lambda e: print(self.global_path.get()))
		# ===== TOP PANEL ===== #

		# ===== MAIN PANEL ===== #
		self.main_panel = tk.Frame(self)
		self.main_panel.pack(side='top', fill='both', expand=tk.ON)
		# ===== MAIN PANEL ===== #

		# ===== BOTTOM PANEL ===== #
		bottom_panel = tk.Frame(self)
		bottom_panel.pack(side='top', fill='x')

		self.cancle_btn = ttk.Button(bottom_panel, text='Отмена')
		self.cancle_btn.pack(side='right', padx=15, pady=10)

		open_btn_frame = tk.Frame(bottom_panel, bg='blue')
		open_btn_frame.pack(side='right', padx=15, pady=10)
		self.open_btn = ttk.Button(open_btn_frame, text='Открыть')
		self.open_btn.pack(padx=1, pady=1)
		# ===== BOTTOM PANEL ===== #

	def create_treeview(self) -> FolderTreeview:
		treeview = FolderTreeview(self.main_panel)
		treeview.pack(side='left', fill='both', expand=tk.ON)

		return treeview


class Manager(tk.Tk):
	def __init__(self, title: str, multiple_choice: bool = True):
		super().__init__()
		self.title(title)

		self.PATH = os.getcwd()

		self.interface = UI(self, self.PATH)
		self.treeview = self.interface.create_treeview()

		self.interface.pack()

		self.treeview.treeview.bind('<Double-1>', self.file_selected)
		self.interface.back_btn.bind('<Button-1>', self.folder_level_up)
		self.interface.open_btn.bind('<Button-1>', self.returnSelectedPath)
		self.interface.cancle_btn.bind('<Button-1>', self.pressCancle)
		self.interface.global_path_entry.bind('<Return>',
			lambda event: self.update_path())

	def update_path(self) -> None:
		path = self.interface.global_path.get()
		# if self.check_valid(path):
		self.PATH = path
		self.update_folder_elements()

	def update_path_entry(self) -> None:
		self.interface.global_path.set(self.PATH)
		self.update_path()

	def update_folder_elements(self) -> None:
		if self.check_valid_dir(self.PATH):
			self.treeview.clear()
			self.treeview.insertElements(self.PATH)
		else:
			mb.showerror('OSError!', 'Incorrect path!')

	def file_selected(self, event: tk.Event) -> None:
		for selection in self.treeview.selection():
			item = self.treeview.item(selection)
			name, _, type = item['values'][:3]
			print(name, type)
			if type == 'Папка с файлами':
				self.PATH = os.path.join(self.PATH, name)
				self.update_path_entry()
				self.update_folder_elements()
			else:
				self.returnSelectedPath(None)

	def check_valid_dir(self, path: str) -> bool:
		if os.path.exists(path) and os.path.isdir(path):
			return True
		return False

	def folder_level_up(self, event: tk.Event) -> None:
		self.PATH = os.path.dirname(self.PATH)
		self.update_folder_elements()
		self.update_path_entry()

	def check_valid(self, path: str) -> bool:
		# TODO: сделать нормально
		if os.path.exists(path):
			if os.path.isfile(path):
				print(f'File "{path}" is exists!')
				return True
			else:
				print(f'"{path}" not file!')
				return False
		else:
			print(f'File "{path}" not found!')
			return False

	def returnSelectedPath(self, event: tk.Event) -> None:
		print(f'Event has type "{type(event)}"')
		path = self.interface.global_path.get()

		if self.check_valid(path):
			self.PATH = path
			self.destroy()
		else:
			# TODO: спросить у пользователя, будет ли он исправлять
			pass

	def pressCancle(self, event: tk.Event) -> None:
		self.destroy()


def askOpenFileName():
	manager = Manager(title='Открыть файл', multiple_choice=False)
	manager.mainloop()

	return manager.PATH


def main():
	path = askOpenFileName()
	print(f'askOpenFileName returned "{path}"')


if __name__ == '__main__':
	main()