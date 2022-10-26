#!/usr/bin/python3

import os
import pyperclip
import requests
import bs4
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter import messagebox as mb

wf = os.path.abspath(__file__)
wd, filename = os.path.split(wf)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'}
item = []
rubrica = 'Ссылки'
rubrica_list = []
link = pyperclip.paste()
item.append(link)

try:
	res = requests.get(link, headers=headers)
except:
	print ('Это не ссылка')
	#show_warning()

res.raise_for_status()
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
	#with open('E:\My\_MEGAsinc\study\python\links\example_clear.html', 'r', encoding='utf-8') as f_in:
	with open(wd + '/example_clear.html', 'r', encoding='utf-8') as f_in:
		contents = f_in.read()
	
soup = bs4.BeautifulSoup(contents, 'lxml')
"""
for i in soup.select('ul'):
	rubrica_list.append(i.get('id'))
rubrica_list.remove('Содержание')
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

#new_link('Ссылки')
#save_link()

# считать содержимое сораненной страницы ссылок +
# по клику на ярлыке записать линк из буфера обмена +
# предложить выбрать группу ссылок
# сформировать HTML страницу. Запиустить страницу в браузере +
