import tkinter as tk, requests, bs4

url =''
string = ''
r = None
sourcecode = ''

def sendMessage(e=None):
	global string
	global url
	global sourcecode
	infobox.delete(0, tk.END)
	string = entry.get()
	if string[0] == ':':
		if string[1:].lower() == 'help':
			display(help_info)
		elif string[1:].lower() == 'version':
			display(version_info)
	if string[0:3] == 'www':
		string = 'http://' + string
	if string[0:4] == 'http':
		url = string
		sourcecode = getSourceCode(url)
		display(sourcecode)
	else:
		display(invalid_info)

def getSourceCode(url):
	global r
	r = requests.get(url)
	return bs4.BeautifulSoup(r.content.decode('utf-8'), 'lxml').prettify()

def display(rawstr):
	consequence = rawstr.split('\n')
	for line in consequence:
		infobox.insert(tk.END, line)

help_info = 'HELP:\nAuthor: Aimishan\nDate: 2017/03/07\n'
version_info = 'Version: 0.0.1'
invalid_info = 'Invaild url address'

win = tk.Tk()
win.title('网站源代码查看器')

entry = tk.Entry(win, width=100)
infobox = tk.Listbox(win, width=90, height=30, background='grey')
scrollbar = tk.Scrollbar(win)
downsidescr = tk.Scrollbar(win, orient=tk.HORIZONTAL)

scrollbar['command'] = infobox.yview
infobox['yscrollcommand'] = scrollbar.set

downsidescr['command'] = infobox.xview
infobox['xscrollcommand'] = downsidescr.set

entry.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)
infobox.grid(row=1, column=0, sticky=tk.N+tk.W+tk.E)
scrollbar.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E)
downsidescr.grid(row=1, column=0, sticky=tk.S+tk.W+tk.E)

entry.bind('<Key-Return>', sendMessage)

win.mainloop()
