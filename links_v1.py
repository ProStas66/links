#!/usr/bin/python3

import os
import pyperclip
import requests
import bs4
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

wf = os.path.abspath(__file__)
wd, filename = os.path.split(wf)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'}
item = []
link = pyperclip.paste()

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
		#links_html(title, opisanie)
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
		self.lbl_url = LabelFrame(text='URL')
		self.lbl_url.pack(anchor=W)
		self.mes_url = Message(self.lbl_url, text=link, width=500)
		self.mes_url.pack()
		self.mes_title = Message(text=self.title, width=500)
		self.mes_title.pack(anchor=W)
		#self.txt_title = Entry(width=60)
		#self.txt_title.insert(0, self.title)
		#self.txt_title.pack()
		self.txt_opis = Text( width=60, height=10)
		self.txt_opis.insert('1.0', self.opisanie)
		self.txt_opis.pack()
		self.btn_ok = Button(text='OK', command=self.make_html)
		self.btn_ok.pack(side=RIGHT)
		self.btn_out = Button(text='Cancel', command=self.killwin)
		self.btn_out.pack(side=RIGHT)
		self.master.mainloop()
		
	def make_html(self):
		with open(link_file(), 'r', encoding='utf-8') as f_in:
			contents = f_in.read()
		soup = bs4.BeautifulSoup(contents, 'lxml')
		
		li_tag = soup.new_tag('li')
		a_tag = soup.new_tag('a', href=link)
		a_tag.string = self.title
		a_tag.string.wrap(soup.new_tag('H3'))
		li_tag.append(a_tag)
		li_tag.append(self.txt_opis.get(1.0, END))
		soup.ul.append(li_tag)
		
		list_li = soup('li')
		list_li = sorted(list_li, key = lambda elem: elem.a.get('href'))
		ul_tag = soup.find('ul')
		ul_tag.clear()
		for elem in list_li:
			ul_tag.append(elem)
		soup = soup.prettify()
		with open ('links.html', 'w', encoding='utf-8') as f_out:
			f_out.write(soup)
		self.killwin()
				
	
	def killwin(self):
		window.destroy()
	
	
		
	
window = Tk()
link_in()
