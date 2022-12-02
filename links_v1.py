#!/usr/bin/python3

import os
import pyperclip
import requests
import bs4
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkhtmlview import HTMLLabel

wf = os.path.abspath(__file__)
wd, filename = os.path.split(wf)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'}
item = []
link = pyperclip.paste()
#link = 'https://gooool.tv'

def link_file():
	if os.path.isfile('links.html'):
		link_file = 'links.html'
	else:
		link_file = wd + '\links_clear.html'
	return link_file

def link_in():
	if type(link) == str and link.startswith('http'):
		res = requests.get(link, headers=headers)
		eSoup = bs4.BeautifulSoup(res.text, 'lxml')
		title = eSoup.title.text
		
		metatags = eSoup.find('meta', attrs={'name':'description'})
		if metatags:
			opisanie = metatags.get('content')
		else:
			opisanie = 'Описание отсутствует'
		Main_win(window, title, opisanie)
	else:
		messagebox.showerror('Это не ссылка!', 'Данные не являются ссылкой')

def links_html(title, opisanie):
	with open(link_file(), 'r', encoding='utf-8') as f_in:
		contents = f_in.read()
	soup = bs4.BeautifulSoup(contents, 'lxml')
	
	li_tag = soup.new_tag('li')
	a_tag = soup.new_tag('a', href=link)
	a_tag.string = title
	a_tag.string.wrap(soup.new_tag('H3'))
	li_tag.append(a_tag)
	li_tag.append(opisanie)
	soup.ul.append(li_tag)
	
	list_li = soup('li')
	list_li = sorted(list_li, key = lambda elem: elem.a.get('href'))
	ul_tag = soup.find('ul')
	print(ul_tag)
	ul_tag.clear()
	for elem in list_li:
		ul_tag.append(elem)
	print('clean:', ul_tag)
	
	soup = soup.prettify()
	with open ('links.html', 'w', encoding='utf-8') as f_out:
		f_out.write(soup)
	print(soup)

class Main_win:
	def __init__(self, master, title, opisanie):
		self.title = title
		self.opisanie = opisanie
		self.master = master
		self.master.title('Описание ссылки')
		self.soup = self.open_links()
		self.list_li = self.soup('li')
		self.lbl_url = LabelFrame(text='URL')
		self.lbl_url.pack(anchor=W)
		self.mes_url = Message(self.lbl_url, text=link, width=500)
		self.mes_url.pack()
		self.mes_title = Message(text=self.title, width=500)
		self.mes_title.pack(anchor=W)
		self.txt_opis = Text( width=60, height=10)
		self.txt_opis.insert('1.0', self.opisanie)
		self.txt_opis.pack()
		self.btn_ok = Button(text='OK', command=self.make_html)
		self.btn_ok.pack(side=RIGHT)
		self.btn_edit = Button(text='Edit', command=self.open_edit)
		self.btn_edit.pack(side=LEFT)
		
		self.chk_state = BooleanVar()
		self.chk_state.set(True)
		self.chk = Checkbutton(text='Добавить ссылку', variable=self.chk_state)
		self.chk.pack(side=RIGHT)

		self.btn_out = Button(text='Cancel', command=self.killwin)
		self.btn_out.pack(side=RIGHT)
		self.master.mainloop()
		
	def open_links(self):
		with open(link_file(), 'r', encoding='utf-8') as f_in:
			contents = f_in.read()
		return bs4.BeautifulSoup(contents, 'lxml')
		
	def new_link(self):
		li_tag = self.soup.new_tag('li')
		a_tag = self.soup.new_tag('a', href=link)
		a_tag.string = self.title
		a_tag.string.wrap(self.soup.new_tag('H3'))
		li_tag.append(a_tag)
		li_tag.append(self.txt_opis.get(1.0, END))
		return li_tag
		
	
	def make_html(self):
		if self.chk_state.get():
			self.list_li.append(self.new_link())
		self.list_li = sorted(self.list_li, key = lambda elem: elem.a.get('href'))
		ul_tag = self.soup.find('ul')
		ul_tag.clear()
		for elem in self.list_li:
			ul_tag.append(elem)
		self.soup = self.soup.prettify()
		with open ('links.html', 'w', encoding='utf-8') as f_out:
			f_out.write(self.soup)
		self.killwin()
	
	def open_edit(self):
		self.editor = Edit_win(self.master, self.list_li)
		self.return_links = self.editor.go()
		if self.return_links:
			self.list_li = self.return_links
		else:
			print('Нет данных')
				
	
	def killwin(self):
		window.destroy()
	
class Edit_win:
	def __init__(self, master, links_list):
		self.slave = Toplevel(master)
		self.slave.title('editor')
		self.links_list = links_list
		self.links = self.len_links()
		self.link_num = 0
		self.new_links = None
		self.html_view = HTMLLabel(self.slave, font=('Arial', 8))
		self.html_view.pack(padx=20)
		self.html_code = Text(self.slave, width='60', height='20')
		self.code_in()
		self.html_code.pack(side=LEFT, padx=20)
		self.html_code.bind('<<Modified>>', self.html_change)
		self.scale_frm = Frame(self.slave, width=10)
		self.scale_frm.pack(side=LEFT)

		self.prev_btn = Button(self.scale_frm, text='Prev', command=lambda: self.links_scale(-1))
		self.prev_btn.pack()
		self.next_btn = Button(self.scale_frm, text='Next', command=lambda: self.links_scale(1))
		self.next_btn.pack()
		self.btn_del = Button(self.slave, text='Delete', width='10', command=self.delete_link)
		self.btn_del.pack(pady=2)
		self.btn_apply = Button(self.slave, text='Apply', width='10', command=self.apply_html)
		self.btn_apply.pack(pady=2)
		self.btn_cancel = Button(self.slave, text='Cancel', width='10', command=self.slave.destroy)
		self.btn_cancel.pack(pady=2)
		self.btn_save = Button(self.slave, text='Save', width='10', command=self.save_links)
		self.btn_save.pack(pady=2)
		self.links_scale(0)
		
	
	def len_links(self):
		lenl = len(self.links_list) - 1
		return lenl
	
	def links_scale(self, a):
		self.link_num += a
		if self.link_num == 0:
			self.prev_btn['state'] = DISABLED
		else:
			self.prev_btn['state'] = NORMAL
		if self.link_num == self.len_links():
			self.next_btn['state'] = DISABLED
		else:
			self.next_btn['state'] = NORMAL
		self.code_in()
	
	def code_in(self):
		self.html_code.delete('0.0', END)
		self.html_code.insert('0.0', self.links_list[self.link_num].prettify())
	
	def apply_html(self):
		soup = bs4.BeautifulSoup(self.html_code.get('1.0', END), 'lxml')
		self.links_list[self.link_num] = soup
	
	def delete_link(self):
		del self.links_list[self.link_num]
		self.code_in()
			
	def save_links(self):
		self.new_links = self.links_list
		self.slave.destroy()
	
	def go(self):
		self.slave.grab_set()
		self.slave.wait_window()
		return self.new_links
	
	def html_change(self, event):
		self.html_code.edit_modified(0)
		self.html_view.set_html(self.html_code.get('1.0', END))
			
		
	
window = Tk()
link_in()
