#!/usr/bin/python3

import os
import pyperclip
import requests
import bs4
from tkinter import *
from tkinter import ttk

#from tkinter.ttk import Progressbar
#from tkinter.ttk import Combobox
from tkinter import messagebox

wf = os.path.abspath(__file__)
wd, filename = os.path.split(wf)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'}
item = []
link = pyperclip.paste()
#link = 'https://sky.pro/head'

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

"""
#rubrica = 'Ссылки'
#rubrica_list = []
#item.append(link)

try:
	res = requests.get(link, headers)
except:
	print ('Это не ссылка')
	#show_warning()

#res.raise_for_status()
print(res)



eSoup = bs4.BeautifulSoup(res.text, 'lxml')
#title = eSoup.find('title').text
title = eSoup.title.text
item.append(title)
metatags = eSoup.find('meta', attrs={'name':'description'})
if metatags:
	opisanie = metatags.get('content')
else:
	opisanie = 'Описание отсутствует'
item.append(opisanie)

try:
	with open('links.html', 'r', encoding='utf-8') as f_in:
		contents = f_in.read()
except IOError:
	#with open('E:\My\_MEGAsinc\study\python\links\links_clear.html', 'r', encoding='utf-8') as f_in:
	with open(wd + '/links_clear.html', 'r', encoding='utf-8') as f_in:
		contents = f_in.read()
	
soup = bs4.BeautifulSoup(contents, 'lxml')
"""

"""
for i in soup.select('ul'):
	rubrica_list.append(i.get('id'))
rubrica_list.remove('Содержание')
"""
"""
def new_link(rubrica):
	newtag_li = soup.new_tag('li')
	newtag_a = soup.new_tag('a', href=link)
	newtag_h3 = soup.new_tag('h3')
	newtag_a.append(newtag_h3)
	newtag_li.append(newtag_a)
	newtag_h3.string = title
	newtag_li.append(opisanie)
	ultag = soup.find('ul', attrs={'id':rubrica})
	ultag.append(newtag_li)
	#print(ultag)

def save_link():
	page_html = soup.prettify()
	#page_html = page_html.encode('utf8')
	with open ('links.html', 'w', encoding='utf-8') as f_out:
		f_out.write(page_html)



def get_text():
	global opisanie
	opisanie = txt_opis.get(1.0, END)
	new_link('Ссылки')
	save_link()
	window.destroy()
    
def show_warning():
	msg = 'Это не ссылка'
	mb.showwarning('Информация', msg)

window = Tk()
window.geometry('500x500')
f_url = LabelFrame(text='URL')
f_url.pack(anchor=W)
mes_url = Message(f_url, text=link, width=480)
mes_url.pack(anchor=W)

mes_title = Message(window, text=title, width=450)
mes_title.pack(anchor=W)

txt_opis = Text(window, width=60, height = 10, wrap='word')
txt_opis.insert('1.0', opisanie)
txt_opis.pack()

but_set = Button(text="OK", command=get_text)
but_set.pack(side=RIGHT)

but_out = Button(text="Cancel", command=window.destroy)
but_out.pack(side=RIGHT)

but_out = Button(text="Test", command=show_warning)
but_out.pack(side=RIGHT)

window.mainloop()








"""

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
		self.txt_title = Entry(width=60)
		self.txt_title.insert(0, self.title)
		self.txt_title.pack()
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
#print(ppp.title)
#Main_win(window)



#new_link('Ссылки')
#save_link()

# считать содержимое сораненной страницы ссылок +
# по клику на ярлыке записать линк из буфера обмена +
# предложить выбрать группу ссылок
# сформировать HTML страницу. Запиустить страницу в браузере +
