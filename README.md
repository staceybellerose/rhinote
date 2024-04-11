# Rhinote - A simple "sticky notes" script in Python

Rhinote is a small, simple Python/Tkinter script that provides virtual
"sticky-notes" on your desktop. It's handy for jotting down quick notes or
holding copied text that you plan to paste elsewhere later. Notes can be
saved (as plain ASCII text) for later viewing/editing with Rhinote or any
other text editor. While many such "sticky-note" programs exist for virtually
all computing platforms, Rhinote is extremely simple, lightweight, and
"keyboard-friendly."

This update of Rhinote has been updated to run on Python 3,
and has several new features available. See
[NEWS](https://github.com/staceybellerose/rhinote/blob/main/NEWS)
for the latest information.

## Usage

On Linux, use a terminal to cd to the directory where rhinote.py lives and type
`python3 rhinote.py` (or `python3 rhinote.py &` to get your command prompt
back). Optionally, you may turn rhinote.py into an executable by placing it
in your `~/bin` directory, renaming it `rhinote`, and making it executable with
(for example) `chmod +x rhinote`.

On Windows, double-clicking on the `rhinote-win.pyw` script should run it,
provided you have Python [installed](https://www.python.org/downloads/windows/).

When the Rhinote note appears, simply start typing, or paste (Ctrl-V) any text
you've already cut/copied to your system clipboard. Rhinote will automatically
wrap words at the ends of lines.

Rhinote offers a set of very simple text and file manipulation tools; all
commands are keyboard-driven. Pressing Ctrl-h at any time will display all
available commands:

* Ctrl-x: Cut selected text
* Ctrl-c: Copy selected text
* Ctrl-v: Paste text from clipboard
* Ctrl-a: Select all text
* Ctrl-Shift-a: Unselect any selected text
* Ctrl-z: Undo
* Ctrl-Shift-z: Redo
* Ctrl-n: Open new (blank) Rhinote
* Ctrl-o: Open file (via a file dialog)
* Ctrl-s: Save current note
* Ctrl-Shift-s: Save current note as filename
* Ctrl-p: Print current note
* Ctrl-h: Display help
* Ctrl-@: Display about message
* Ctrl-B: Browse to this repository
* Ctrl-W: Close the current note
* Ctrl-Q: Quit the program, closing all notes

## Modifying Rhinote

Currently, there is no mechanism to change the configuration of Rhinote. If
you want to make changes, the only way is by modifying the source code. Most
of the changable items are set up as constants at the top of the program, and
can easily be changed.

### Change the Note Colors

The default colors for the notes cycle through various pastel color, chosen
to mimic paper sticky-notes. With the `COLOR` constant. you can replace the
list with your own set of colors, or just a single color if you prefer.
(Make sure to keep the square brackets if you use a single color, or the
program will break.)

### Change the Window Size

If you prefer the note windows to be a different size, you can change the
`GEOMETRY` constant. The format is {width}x{height}, and is in pixels.

### Change the Font

If you don't have [Source Sans Pro](https://github.com/adobe-fonts/source-sans)
installed, or prefer to use a different font, you can change it using the `FONT`
constant. The font name is inside the curly braces, and the font size is after
that.

### Disable Word Wrapping

If you prefer to have no word wrapping, or want character-based wrapping
instead of word-based, you can change the `WRAP` constant. Use `tk.CHAR` for
character-based wrapping, and `tk.NONE` to disable wrapping completely. Note
that no scroll bar will appear in the note window, so disabling wrapping is
not advisable.

## Linux Users

Add this to your desktop menu:

```bash
cp rhinote.py $HOME/.local/bin/rhinote
cp rhinote.desktop $HOME/.local/share/applications/
cp icons/rhinote_48x48.png $HOME/.local/share/icons/rhinote.png
```

### Printing on Linux

Rhinote offers a very rudimentary printing "system" (if you want to call it
that). It uses the `enscript` program to format the text, then passes the
result to `lp` (or `lpr` if `lp` is not found) for printing. If you don't have
`enscript` installed, Rhinote will print using `lp`/`lpr` directly (so no
fancy formatting). As long as you have these two programs installed (most
Linux distributions do), Rhinote notes will print on your default printer.

## Windows Users

A wrapper script, `rhinote-win.pyw`, is provided to run under Windows. This
script, with the `pyw` extension, allows Rhinote to run without a console
window appearing. If you want to make changes to the code, you can run
`rhinote.py` directly, and see any messages in a console window.

### Printing on Windows

Print functionality requires the use of `pywin32`. Please install the latest
version using `pip`. If you attempt to print without install `pywin32`, you
will get an error message reminding you to install it.

```cmd
pip install pywin32
```

The actual print process uses Windows Notepad to print a temporary text file,
which is stored in your user folder.

## Historical Notes

The original website is inaccessible, but can be found via the
[Wayback Machine](https://web.archive.org/web/20190125180629/http://rhinote.tuxfamily.org/index.html).

The original README file can be found
[here](https://github.com/staceybellerose/rhinote/blob/main/README.ORIG).

The original documentation file can be found
[here](https://github.com/staceybellerose/rhinote/blob/main/rhinote-doc.html).
