from cProfile import label
from cgitb import text
from concurrent.futures import thread
from ctypes import alignment
from distutils import command
from email import message
from faulthandler import disable
from glob import glob
from textwrap import wrap
from tkinter import *
import tkinter
from tkinter.tix import TEXT
from tkinter.ttk import Style
from turtle import back, left, width
import random

from messageHandler import messageHandler
import time
import socket
import threading
import os

thread1 = threading.Thread()

windowTitle = 'Port Tester'
windowSize = '225x550'
fontSize = 12
fontFamily = 'Arial'

lastPickedRole = ''
roles = {
    'Server':0,
    'Client':1
}


protocols = {
    'TCP':0,
    'UDP':1
}

window = Tk()
protocolRequest = IntVar()
roleRequest = IntVar()
actionButtonText = StringVar()
messageRequest = messageHandler()
hostnameLabelText = StringVar()
hostnameText = StringVar()
savedServerHostname = ''
savedClientHostname = ''
portText = StringVar()
consoleText = Text()
lastPickedRole = 'Server'

def onRoleChange():
    global lastPickedRole
    global savedClientHostname
    global savedServerHostname

    if lastPickedRole == 'Server':
        savedServerHostname = hostnameText.get()
    elif lastPickedRole == 'Client':
        savedClientHostname = hostnameText.get()
    if roleRequest.get() == roles['Server']:
        hostnameText.set(savedServerHostname)
        actionButtonText.set('Receive Message')
        hostnameLabelText.set('Starting Server On:')
        lastPickedRole = 'Server'
    elif roleRequest.get() == roles['Client']:
        hostnameText.set(savedClientHostname)
        actionButtonText.set('Send Message')
        hostnameLabelText.set('Sending To:')
        lastPickedRole = 'Client'

    
def updateConsole(message):
    consoleText.config(state=NORMAL)
    consoleText.delete("1.0", END)
    consoleText.insert(END, message)
    consoleText.config(state=DISABLED)
    window.update()

def threadWrapperServer():
    try:
        updateConsole('Listening...')
        data = None
        addr = None
        if protocolRequest.get() == protocols['UDP']:
            data, addr = messageRequest.receiveUDP(hostnameText.get(), int(portText.get()), 10)
        elif protocolRequest.get() == protocols['TCP']:
            data, addr = messageRequest.receiveTCP(hostnameText.get(), int(portText.get()), 10)
        if len(data) > 0:
            updateConsole('Listening stopped.\nClient: ' + str(addr) + '\nMessage: ' + data.decode())
        else:
            updateConsole('Connection established, nothing was received')
    except Exception as e:
        updateConsole("Error: " + str(e))


    
def onAction():
    try:
        if roleRequest.get() == roles['Server']:
            global thread1
            if thread1.is_alive():
                updateConsole("Server is currently running. Please try again later.")
            else:
                thread1 = threading.Thread(target=threadWrapperServer)
                thread1.start()

        elif roleRequest.get() == roles['Client']:
            sendMessage = str(random.getrandbits(64))
            updateConsole("Sending message...")
            if protocolRequest.get() == protocols['UDP']:
                messageRequest.sendUDP(hostnameText.get(), sendMessage, int(portText.get()), 5)
            elif protocolRequest.get() == protocols['TCP']:
                messageRequest.sendTCP(hostnameText.get(), sendMessage, int(portText.get()), 5)
            updateConsole("Sent to: " + hostnameText.get() + "\nMessage: " + sendMessage)
    except Exception as e:
        updateConsole("Error: " + str(e))
        

# Create window 
window.title(windowTitle)
window.geometry(windowSize)
window.lift()
window.resizable(False, False)
actionButtonText.set('Receive Message')

# Hostname
hostnameLabelText.set('Starting Server On:')
Label(window, textvariable=hostnameLabelText, font=(fontFamily, fontSize), justify=LEFT, padx=20).pack(anchor='w')
Entry(window, textvariable=hostnameText, font=(fontFamily, fontSize)).pack(anchor='w', padx=20, pady=(0,10))
hostnameText.set(socket.gethostname())

# Port
portText.set('8080')
Label(window, text='Port:', font=(fontFamily, fontSize), justify=LEFT, padx=20).pack(anchor='w')
Entry(window, textvariable=portText, font=(fontFamily, fontSize)).pack(anchor='w', padx=20, pady=(0,10))

# Role form
Label(window, text='Role', font=(fontFamily, fontSize), justify=LEFT, padx=20).pack(anchor='w')
for role, value in roles.items():
    Radiobutton(window,
    text=role,
    padx=40,
    variable=roleRequest,
    value=value,
    font=(fontFamily, fontSize),
    command=onRoleChange
    ).pack(anchor='w')   

# Protocol form 
Label(window, text='Protocol', font=(fontFamily, fontSize), justify=LEFT, padx=20).pack(anchor='w')
for protocol, value in protocols.items():
    Radiobutton(window,
    text=protocol,
    padx=40,
    variable=protocolRequest,
    value=value,
    font=(fontFamily, fontSize)
    ).pack(anchor='w')

# Console
Label(window, text='Console: ', font=(fontFamily, fontSize), justify=LEFT, padx=20).pack(anchor='w')
consoleText = Text(window, width=25, height=10, state=DISABLED, wrap=WORD)
consoleText.pack(anchor='w', padx=20)

# Action Button 
Button(window,textvariable=actionButtonText, font=(fontFamily, fontSize), command=onAction).pack(anchor='w', padx=20, pady=20)
window.mainloop()


