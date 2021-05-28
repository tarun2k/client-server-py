# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:53:31 2020

@author: Tarun Arora
"""

import tkinter as tk
import socket

class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,str):
        self.text_area.insert("end", str)
    def flush(self):
        pass

def redirector(inputStr):
    import sys
    root = tk.Toplevel()
    T = tk.Text(root)
    sys.stdout = StdoutRedirector(T)
    T.pack()
    T.insert(tk.END, inputStr)

def client_call(stock_code, city_name):
    host = 'local host'
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port)) 

    code = stock_code
    city = city_name

    f_inp = code + '\n' +city
    s.send(f_inp.encode())

    print(s.recv(20480).decode())

    s.close()

def show_results(master, stockCode, Cityname):

    r = redirector('Running application\n')
    # Before invoking banner function, redirect stdout to result_box
    client_call(stockCode.get(), Cityname.get())

master = tk.Tk()
master.title("Client Server Application to get daily news, stock price and weather updates")

tk.Label(master,
         text="Please enter Stock code: ").grid(row=0)

stockCode = tk.Entry(master)
stockCode.grid(row=1)

tk.Label(master,
         text="Please enter City name: ").grid(row=2)

Cityname = tk.Entry(master)
Cityname.grid(row=3)

scrollbar = tk.Scrollbar(master)

tk.Button(master, text="Ok", command=lambda: show_results(master, stockCode, Cityname)).grid(row=4)
scrollbar.config( command = lambda: show_results(master, stockCode, Cityname) )
tk.mainloop()