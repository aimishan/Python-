import tkinter as tk, requests, bs4

url =''
string = ''
r = None
sourcecode = ''
webpage_info = ''

def sendMessage(e=None):
	global string
	global url
	global sourcecode
	global webpage_info
	global r
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
		webpage_info = getHeaders(r)
		display(sourcecode)
		display(webpage_info, 1)
	else:
		display(invalid_info)

def getSourceCode(url):
	global r
	r = requests.get(url)
	return bs4.BeautifulSoup(r.content.decode('utf-8'), 'lxml').prettify()

def getHeaders(req):
	tmp = ''
	for key in req.headers.keys():
		tmp = tmp + key + '\n' + '     ' + req.headers[key] + '\n'
	return tmp

def display(rawstr, index=0):
	consequence = rawstr.split('\n')
	if index == 0:
		for line in consequence:
			infobox.insert(tk.END, line)
	else:
		for line in consequence:
			headerinfo.insert(tk.END, line)

help_info = 'HELP:\nAuthor: Aimishan\nDate: 2017/03/07\n'
version_info = 'Version: 0.0.1'
invalid_info = 'Invaild url address'

win = tk.Tk()
win.title('网站源代码查看器')

entry = tk.Entry(win, width=100)
infobox = tk.Listbox(win, width=90, height=35, background='grey')
scrollbar = tk.Scrollbar(win)
downsidescr = tk.Scrollbar(win, orient=tk.HORIZONTAL)
headerinfo = tk.Listbox(win, width=40)
headerscr = tk.Scrollbar(win, orient=tk.HORIZONTAL)

scrollbar['command'] = infobox.yview
infobox['yscrollcommand'] = scrollbar.set

downsidescr['command'] = infobox.xview
infobox['xscrollcommand'] = downsidescr.set

headerscr['command'] = headerinfo.xview
headerinfo['xscrollcommand'] = headerscr.set

entry.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)
infobox.grid(row=1, column=0, sticky=tk.N+tk.W+tk.E)
scrollbar.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E)
downsidescr.grid(row=1, column=0, sticky=tk.S+tk.W+tk.E)
headerinfo.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S+tk.W)
headerscr.grid(row=1, column=1, sticky=tk.W+tk.E+tk.S)

entry.bind('<Key-Return>', sendMessage)

win.mainloop()
