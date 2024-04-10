#!/usr/bin/env python
# Filename : rhinote.py

# Rhinote version 0.7.4  A simple "sticky notes" application; Windows version.

# Copyright 2006, 2010 by Marv Boyes - greyspace@tuxfamily.org
# http://rhinote.tuxfamily.org
# Please see the file COPYING for license details.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# Thiis program is distributed in hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULR PURPOSE. See the 
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free SOftware
# Foundation, Inc., 51 Franklin St., Fifth Floor, Boston, MA  02110-1301 USA

from Tkinter import *
import tkFileDialog, tkMessageBox
import os
from os import system

# the root window:
def Rhinote():
    r = Tk()
    r.option_add('*font', '{Helvetica} 11')
    t = TextWidget(r, bg = '#f9f3a9', wrap = 'word', undo = True)
    t.focus_set()
    t.pack(fill = 'both', expand = 1)
    r.geometry('220x235')
    r.title('Rhinote')
    r.mainloop()

# the text widget, and all of its functions:
class TextWidget(Text):

    def save_file(self, whatever = None):
        if (self.filename == ''):
            self.save_file_as()
            self.master.title('Rhinote %s' % self.filename)
        else:
            f = open(self.filename, 'w')
            f.write(self.get('1.0', 'end'))
            f.close()
            self.master.title('Rhinote %s' % self.filename)
            # Comment out the following line if you don't want a 
            # pop-up message every time you save a file:
            tkMessageBox.showinfo('FYI', 'File Saved.')

    def save_file_as(self, whatever = None):
        self.filename = tkFileDialog.asksaveasfilename(filetypes = self._filetypes)
        f = open(self.filename, 'w')
        f.write(self.get('1.0', 'end'))
        f.close()
        # comment out the following line if you don't want a
        # pop-up message every time you save a file:
        tkMessageBox.showinfo('FYI', 'File Saved')

    def open_file(self, whatever = None, filename = None):
        if not filename:
            self.filename = tkFileDialog.askopenfilename(filetypes = self._filetypes)
            self.master.title('Rhinote %s' % self.filename)
        else:
            self.filename = filename
            self.master.title('Rhinote %s' % self.filename)
        if not (self.filename == ''):
            f = open(self.filename, 'r')
            f2 = f.read()
            self.delete('1.0', 'end')
            self.insert('1.0', f2)
            f.close()
            self.master.title('Rhinote %s)' % self.filename)

    def new_window(self, event):
        Rhinote()

    def help(self, whatever = None):
        tkMessageBox.showinfo('Rhinote Help', message = '''
Editing Commands
    Ctrl-x : Cut selected text
    Ctrl-c : Copy selected text
    Ctrl-v : Paste cut/copied text
    Ctrl-Z : Undo
    Ctrl-Shift-z : Redo

File Commands
    Ctrl-o : Open file
    Ctrl-s : Save current note
    Ctrl-a : Save current note as <filename>
    Ctrl-n : Open new Rhinote

General
    Ctrl-h : Display this help window

Rhinote version 0.7.4
Free Software distributed under the GNU General Public License
http://rhinote.tuxfamily.org
''')

    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-n>', self.new_window)
        self.bind('<Control-N>', self.new_window)
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-O>', self.open_file)
        self.bind('<Control-s>', self.save_file)
        self.bind('<Control-S>', self.save_file)
        self.bind('<Control-a>', self.save_file_as)
        self.bind('<Control-A>', self.save_file_as)
        self.bind('<Control-h>', self.help)
        self.bind('<Control-H>', self.help)
        self.master = master
        self.filename = ''
        self._filetypes = [
        ('Text/ASCII', '*.txt'),
        ('Rhinote files', '*.rhi'),
            ('All files', '*'),
            ]

# make it so:
if __name__ == '__main__':
    Rhinote()

