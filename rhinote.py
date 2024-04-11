#!/usr/bin/env python3

'''
Rhinote - A simple "sticky notes" application.

Copyright 2006, 2010 by Marv Boyes - greyspace@tuxfamily.org http://rhinote.tuxfamily.org
Copyright 2024 by Stacey Adams - stacey.belle.rose@gmail.com
Please see the file LICENSE for license details.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St., Fifth Floor, Boston, MA  02110-1301 USA
'''

from __future__ import annotations

import platform
import shutil
import subprocess
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, font, messagebox

PRINT_AVAILABLE = True

if platform.system() == 'Windows':
    try:
        import win32api
        import win32print
    except ImportError:
        PRINT_AVAILABLE = False

__version__ = '0.8.0'

COLORS = ['#f9a9f9', '#a9f9f9', '#f9f9a9', '#a9a9f9', '#a9f9a9', '#f9a9a9']
GEOMETRY = '330x235'
FONT = '{Source Sans Pro} 11'
WRAP = tk.WORD  # can be tk.WORD, tk.CHAR, or tk.NONE
APP_NAME = 'Rhinote'
NOTE_LIST: list[TextWidgetContainer] = []
REPO_URL = 'https://github.com/staceybellerose/rhinote'


class ContentPrinter:
    '''A wrapper for the various print methods available.'''

    def __init__(self, contents: str) -> None:
        if not PRINT_AVAILABLE:
            messagebox.showerror(
                f'{APP_NAME} print error',
                'Printing is not available. Please install pywin32 and reload '
                    'this program.'
            )
        self.contents = contents
        self.print_command = shutil.which('lp')
        self.print_args = ['-t', f'{APP_NAME} file']
        if not self.print_command:
            self.print_command = shutil.which('lpr')
            self.print_args = ['-T', f'{APP_NAME} file']
        self.format_command = shutil.which('enscript')
        self.format_args = ['--noheader', '--word-wrap', '-p', '-']

    def print(self):
        '''Print the provided contents.'''
        if platform.system() == 'Windows':
            self.print_windows()
            return
        if not self.print_command:
            messagebox.showerror(
                f'{APP_NAME} print error', 'Print command (lp or lpr) not found'
            )
            return
        # Prepare the print command
        print_argv = [self.print_command]
        print_argv.extend(self.print_args)
        if self.format_command:
            # Prepare the format command
            format_argv = [self.format_command]
            format_argv.extend(self.format_args)
            # Spawn both commands, piping the output of the format command
            with subprocess.Popen(print_argv, stdin=subprocess.PIPE) as pp:
                with subprocess.Popen(
                    format_argv, stdin=subprocess.PIPE, stdout=pp.stdin
                ) as fp:
                    fp.communicate(input=self.contents.encode())
                    pp.communicate()
                    if fp.returncode > 0 or pp.returncode > 0:
                        messagebox.showerror(
                            f'{APP_NAME} print error', 'Printing failed'
                        )
            return
        # no enscript, so just use lp/lpr
        with subprocess.Popen(print_argv, stdin=subprocess.PIPE) as pp:
            pp.communicate(input=self.contents.encode())
            if pp.returncode > 0:
                messagebox.showerror(f'{APP_NAME} print error', 'Printing failed')

    def print_windows(self):
        '''Print the contents in MS Windows.'''
        printfile = Path.home() / '.Rhinoteprintfile.txt'
        with printfile.open('w', encoding='UTF-8') as f:
            f.write(self.contents)
            f.flush()
        # This only works if the file extension is associated with an
        # application that can print. Since we are saving to a *.txt file,
        # we should be OK.
        win32api.ShellExecute(
            0, 'print', str(printfile), f'/d:{win32print.GetDefaultPrinter()}',
            '.', 0
        )


class TextWidgetContainer:
    '''A toplevel widget that contains a TextWidget.'''

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        NOTE_LIST.append(self)
        self.init_window()
        bgcolor = COLORS[len(NOTE_LIST) % len(COLORS)]
        self.text_widget = TextWidget(self, bg=bgcolor)
        self.text_widget.focus_set()
        self.text_widget.pack(fill='both', expand=1)
        self.toplevel = self.text_widget.winfo_toplevel()
        self.toplevel.protocol('WM_DELETE_WINDOW', self.save_before_close)
        self.toplevel.bind('<Control-n>', self.new_window)
        self.toplevel.bind('<Control-w>', self.close)
        self.toplevel.bind('<Control-q>', self.close_all)
        self.toplevel.bind('<Control-h>', self.help)
        self.toplevel.bind('<Control-at>', self.about)

    def init_window(self): ...

    def save_before_close(self):
        '''Save the note before closing this window.'''
        if self.text_widget.edit_modified():
            if messagebox.askyesno(
                APP_NAME,
                'Note has not been saved. Do you wish to save before closing?',
                parent=self
            ):
                self.text_widget.save_file(None)
        NOTE_LIST.remove(self)
        self.toplevel.destroy()

    def close(self, *_args):
        '''Close this note window.'''
        self.save_before_close()

    def close_all(self, *_args):
        '''Close all the note windows.'''
        for note in reversed(NOTE_LIST):
            note.save_before_close()

    def new_window(self, *_args):
        '''Create a new note window.'''
        Rhinote()

    def help(self, *_args):
        '''Display a help message with available commands.'''
        messagebox.showinfo(
            f'{APP_NAME} Help',
            message='Editing Commands\n'
                'Ctrl-x : Cut selected text\n'
                'Ctrl-c : Copy selected text\n'
                'Ctrl-v : Paste cut/copied text\n'
                'Ctrl-z : Undo\n'
                'Ctrl-Shift-z : Redo\n'
                '\n'
                'File Commands\n'
                'Ctrl-o : Open file\n'
                'Ctrl-s : Save current note\n'
                'Ctrl-Shift-s : Save current note with new filename\n'
                'Ctrl-p : Print current note\n'
                f'Ctrl-n : Open new {APP_NAME} window\n'
                '\n'
                'General\n'
                'Ctrl-h : Display this help window\n'
                'Ctrl-@ : Display About box\n'
                'Ctrl-w : Close current note\n'
                f'Ctrl-q : Quit {APP_NAME}',
            parent=self.toplevel
        )

    def about(self, *_args):
        '''Display a simple About messagebox.'''
        messagebox.showinfo(
            f'About {APP_NAME}',
            message=f'{APP_NAME} version {__version__}\n'
                '\n'
                'Free Software distributed under the '
                'GNU General Public License version 2\n'
                '\n'
                f'{REPO_URL}'
        )

class RhinoteApp(TextWidgetContainer, tk.Tk):
    '''The main application, which contains a TextWidget.'''

    def __init__(self) -> None:
        super().__init__(className=APP_NAME)
        self.geometry(GEOMETRY)
        self.title(APP_NAME)
        self.iconphoto(
            True, tk.PhotoImage(
                file=Path(__file__).parent / "icons" / "rhinote_32x32.png"
            )
        )

    def init_window(self):
        self.option_add('*font', FONT)
        self.option_add("*tearOff", False)  # Fix menus


class Rhinote(TextWidgetContainer, tk.Toplevel):
    '''A Toplevel widget that contains a TextWidget.'''

    def __init__(self) -> None:
        super().__init__()
        self.geometry(GEOMETRY)
        self.title(APP_NAME)

    def init_window(self):
        pass


# the text widget, and all of its functions:
class TextWidget(tk.Text):
    '''Custom Text widget with editing commands.'''

    def __init__(self, master, **kw):
        super().__init__(
            master, relief=tk.FLAT, wrap=WRAP, undo=True, maxundo=-1,
            selectbackground='#0080ff', selectforeground='#ffffff', **kw
        )
        self.container = master if isinstance(master, TextWidgetContainer) else None
        self.filename = ''
        self.original_content = ''
        self._filetypes = [
            ('Text/ASCII', '*.txt'),
            (f'{APP_NAME} files', '*.rhi'),
            ('All files', '*'),
        ]
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-s>', self.save_file)
        self.bind('<Control-Shift-S>', self.save_file_as)
        self.bind('<Control-p>', self.print_file)
        self.bind('<Control-a>', self.select_all)
        self.bind('<Control-Shift-A>', self.select_none)
        self.bind('<Control-b>', self.browse_repo)
        self.bind('<KeyRelease>', self.set_title, '+')
        self.create_menu()

    def create_menu(self):
        '''Create the right-click menu.'''
        menu = tk.Menu(self, activeborderwidth=0)
        bold = font.Font(font='TkMenuFont', name='boldMenuFont')
        bold.config(weight='bold')
        menu.add_command(label='File', font=bold, state=tk.DISABLED)
        menu.add_command(
            label='New Note', accelerator='Ctrl-N',
            command=self.container.new_window
        )
        menu.add_command(
            label='Open', accelerator='Ctrl-O', command=self.open_file
        )
        menu.add_command(
            label='Save', accelerator='Ctrl-S', command=self.save_file
        )
        menu.add_command(
            label='Save As…', accelerator='Ctrl-Shift-S',
            command=self.save_file_as
        )
        menu.add_command(
            label='Print', accelerator='Ctrl-P', command=self.print_file
        )

        menu.add_command(
            label='Edit', font=bold, state=tk.DISABLED, columnbreak=1
        )
        menu.add_command(
            label='Cut', accelerator='Ctrl-X', command=self.cut
        )
        menu.add_command(
            label='Copy', accelerator='Ctrl-C', command=self.copy
        )
        menu.add_command(
            label='Paste', accelerator='Ctrl-V', command=self.paste
        )
        menu.add_command(
            label='Select All', accelerator='Ctrl-A', command=self.select_all
        )
        menu.add_command(
            label='Select None', accelerator='Ctrl-Shift-A',
            command=self.select_none
        )
        menu.add_command(
            label='Undo', accelerator='Ctrl-Z', command=self.edit_undo
        )
        menu.add_command(
            label='Redo', accelerator='Ctrl-Shift-Z', command=self.edit_redo
        )

        menu.add_command(
            label='Misc', font=bold, state=tk.DISABLED, columnbreak=1
        )
        menu.add_command(
            label='Help…', accelerator='Ctrl-H', command=self.container.help
        )
        menu.add_command(
            label='About…', accelerator='Ctrl-@', command=self.container.about
        )
        menu.add_command(
            label='Browse Repo', accelerator='Ctrl-B', command=self.browse_repo
        )
        menu.add_command(
            label='Close', accelerator='Ctrl-W', command=self.container.close
        )
        menu.add_command(
            label='Quit', accelerator='Ctrl-Q', command=self.container.close_all
        )
        if self.winfo_toplevel().tk.call('tk', 'windowingsystem') == 'aqua':
            # MacOS numbers the right button as 2, rather than 3.
            self.bind(
                '<Button-2>',
                lambda event: menu.tk_popup(event.x_root, event.y_root, 0)
            )
        else:
            self.bind(
                '<Button-3>',
                lambda event: menu.tk_popup(event.x_root, event.y_root, 0)
            )

    def set_title(self, *_args):
        '''Set the title of the window based on the file name.'''
        current_content = self.get('1.0', 'end-1c')
        modified_flag = '*' if current_content != self.original_content else ''
        self.winfo_toplevel().title(f'{APP_NAME} {self.filename} {modified_flag}'.strip())

    def save_named_file(self, filename: str):
        '''Save the note to a specified file name.'''
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(self.get('1.0', 'end'))
            f.flush()
            self.filename = filename
            self.original_content = self.get('1.0', 'end')
            self.set_title()

    def save_file(self, *_args):
        '''Save the note.'''
        if self.filename == '':
            self.save_file_as()
        else:
            self.save_named_file(self.filename)

    def save_file_as(self, *_args):
        '''Save the note with a different file name.'''
        filename = filedialog.asksaveasfilename(filetypes = self._filetypes)
        if filename:
            self.save_named_file(filename)

    def open_file(self, *_args):
        '''Open a file into the current note window.'''
        if self.edit_modified():
            if messagebox.askyesno(
                APP_NAME,
                'Existing note has not been saved. '
                    'Do you wish to save before opening another file?',
                parent=self
            ):
                self.save_file(None)
        filename = filedialog.askopenfilename(filetypes = self._filetypes)
        if filename:
            with open(filename, 'r', encoding='UTF-8') as f:
                contents = f.read()
                self.delete('1.0', 'end')
                self.insert('1.0', contents)
                self.edit_modified(False)  # newly-loaded file isn't modified
                self.original_content = contents
            self.filename = filename
            self.set_title()

    def print_file(self, *_args):
        '''Print the file.'''
        ContentPrinter(self.get('1.0', 'end')).print()

    def cut(self, *_args):
        '''Cut the selected text.'''
        self.event_generate('<<Cut>>')

    def copy(self, *_args):
        '''Copy the selected text.'''
        self.event_generate('<<Copy>>')

    def paste(self, *_args):
        '''Paste the text from the clipboard.'''
        self.event_generate('<<Paste>>')

    def select_all(self, *_args):
        '''Select all the text in the widget.'''
        self.tag_add(tk.SEL, "1.0", "end-1c")

    def select_none(self, *_args):
        '''Clear selection in the widget.'''
        self.tag_delete(tk.SEL)

    def browse_repo(self, *_args):
        '''Open the source code repository for this application.'''
        webbrowser.open_new_tab(REPO_URL)


if __name__ == '__main__':
    app = RhinoteApp()
    app.mainloop()
