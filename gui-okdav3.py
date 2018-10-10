#!/usr/bin/env python3
# Github: https://github.com/undefinedvalue0103/okdacrypt
from tkinter import Tk, Text, Label, Button, Entry
from okdav3 import (decode as ok_decode, encode as ok_encode)
from time import time
from traceback import format_exc

themes = [
    dict(
        background='#262626',
        encoded='#fa5f5f',
        decoded='#5f5ffa',
        key='#5ffa5f',
        status='#5ffafa'),
    dict(
        background='#aaaaaa',
        encoded='#770000',
        decoded='#000077',
        key='#007700',
        status='#007777')
]

root = Tk()
root.title('OKDACrypt v 3.0')
root.geometry('600x400')
root.resizable(False, False)
inputkey = Entry(root, highlightthickness=0, relief='flat', font='monospace 10')
inputkey.place(x=0, y=0, width=575, height=25)
inputdecoded = Text(root, highlightthickness=0, font='monospace 10')
inputdecoded.place(x=0, y=25, width=300, height=350)
inputencoded = Text(root, highlightthickness=0, font='monospace 10')
inputencoded.place(x=300, y=25, width=300, height=350)
statusbar = Label(root, highlightthickness=0, relief='flat', font='monospace 10')
statusbar.place(x=0, y=375, width=600, height=25)

def apply_theme(thm):
    theme = themes[thm]
    thm_btn.config(background=theme['background'], activebackground=theme['background'])
    inputkey.config(background=theme['background'], foreground=theme['key'])
    inputencoded.config(background=theme['background'], foreground=theme['encoded'])
    inputdecoded.config(background=theme['background'], foreground=theme['decoded'])
    statusbar.config(background=theme['background'], foreground=theme['status'])
thm = 0
def swaptheme(ev=None):
    global thm
    thm = 1 - thm
    apply_theme(thm)
thm_btn = Button(root,
    command=swaptheme,
    highlightthickness=0,
    text='T',
    foreground='#777',
    activeforeground='#666',
    relief='flat',
    font='monospace 16')
thm_btn.place(x=575, y=0, width=25, height=25)

def status(text):
    statusbar['text'] = text

lastaction = 'e'
def encode(ev=None):
    global lastaction
    starttime = time()
    lastaction = 'e'
    key = bytes(inputkey.get(), 'utf-8')
    if not key:
        status('Empty key!')
        return
    try:
        message = bytes(inputdecoded.get('1.0', 'end'), 'utf-8')
        encoded = ok_encode(message, key)
        inputencoded.delete('1.0', 'end')
        inputencoded.insert('end', encoded)
        status('Encoded in %dms.'%int((time() - starttime) * 1000))
    except Exception as e:
        status('E: ' + type(e).__name__ + ': ' + str(e))
        print(format_exc())
def decode(ev=None):
    global lastaction
    starttime = time()
    lastaction = 'd'
    key = bytes(inputkey.get(), 'utf-8')
    if not key:
        status('Empty key!')
        return
    try:
        message = inputencoded.get('1.0', 'end').replace('\n', '')
        decoded = ok_decode(message, key)
        inputdecoded.delete('1.0', 'end')
        inputdecoded.insert('end', decoded.decode('utf-8'))
        status('Decoded in %dms.'%int((time() - starttime) * 1000))
    except Exception as e:
        status('D: ' + type(e).__name__ + ': ' + str(e))
        print(format_exc())
        print('message =', message)
def updatekey(ev=None):
    if lastaction == 'e':
        encode()
    else:
        decode()

inputkey.bind('<KeyRelease>', updatekey)
inputdecoded.bind('<KeyRelease>', encode)
inputencoded.bind('<KeyRelease>', decode)

inputkey.insert('end', 'OKDA')
inputdecoded.insert('end', 'Hello, world!')
encode()
apply_theme(thm)
status('Ready.')
root.mainloop()
