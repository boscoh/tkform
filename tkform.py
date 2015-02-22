#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
tkform provides an HTML-inspired form-based GUI
for Python scripts.

Includes
- scrollable page
- simple entry of params
- reordable lists of files or directories
"""


import os
import traceback
import re
import collections

import Tkinter as tk
import tkFileDialog


class VerticalScrolledFrame(tk.Frame):

    """
    A Tkinter scrollable frame:

    - place widgets in the 'interior' attribute
    - construct and pack/place/grid normally
    - only allows vertical scrolling
    - adapted from http://stackoverflow.com/a/16198198
    """

    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)

        self.canvas = tk.Canvas(
            self, bd=0, highlightthickness=0,
            yscrollcommand=vscrollbar.set,
            xscrollcommand=hscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled
        self.interior = tk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(
            0, 0, window=self.interior, anchor=tk.NW)

        # track changes to canvas, frame and updates scrollbar
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # pixels '2', millimeters '2m', centimeters '2c', or inches '2i'
        self.canvas.configure(yscrollincrement='8')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta), "units")

    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(),
                self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(
                self.interior_id, width=self.canvas.winfo_width())


def is_event_in_widget(event, widget):
    x, y = event.x_root, event.y_root
    y0 = widget.winfo_rooty()
    y1 = widget.winfo_height() + y0
    x0 = widget.winfo_rootx()
    x1 = widget.winfo_width() + x0
    return y0 <= y <= y1 and x0 <= x <= x1


class LabeledEntryForList():

    """
    A row that holds a labeld entry and be draggable by mouse.
    This works intimately with ReorderableLabeledList.
    """

    def __init__(self, parent, fname, label=None):
        self.parent = parent

        self.num_stringvar = tk.StringVar()
        self.num_stringvar.set('')
        self.num_widget = tk.Label(parent, textvariable=self.num_stringvar)

        self.fname = fname
        self.fname_widget = tk.Label(parent, text=self.fname)

        self.label = label
        self.label_stringvar = tk.StringVar()
        if self.label is None:
            self.label_stringvar.set('')
        else:
            self.label_stringvar.set(label)
            self.label_widget = tk.Entry(
                parent, textvariable=self.label_stringvar)

        self.delete_widget = tk.Label(parent, text="  x")

    def add_to_grid(self, j):
        self.num_stringvar.set(u'\u2195')
        self.j = j
        self.num_widget.grid(column=0, row=j, sticky='W')
        self.fname_widget.grid(column=1, row=j, sticky='W')
        if self.label is not None:
            self.label_widget = tk.Entry(
                self.parent, textvariable=self.label_stringvar)
            self.label_widget.grid(column=2, row=j, sticky='W')
        self.delete_widget.grid(column=3, row=j, sticky='W')

    def grid_forget(self):
        self.fname_widget.grid_forget()
        self.delete_widget.grid_forget()
        if self.label is not None:
            self.label_widget.destroy()
        self.num_widget.grid_forget()

    def in_y(self, event):
        y = event.y_root
        y0 = self.num_widget.winfo_rooty()
        y1 = self.num_widget.winfo_height() + y0
        return y0 <= y <= y1

    def contains_event(self, event):
        return is_event_in_widget(event, self.num_widget)


class ReorderableLabeledList(tk.Frame):

    """
    This is a table that contains rows of LabeledEntryForList. The rows
    - can be reordered by dragging on the arrow character on
    the left
    - deleted by clicking on the x on the right
    - dynamically added to through `add_entry_label`
    """

    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.grid()
        self.entries = []

    def add_entry_label(self, entry, label=None):
        param = LabeledEntryForList(self, entry, label)
        self.entries.append(param)
        self.clear_frame()
        self.build_frame()

    def clear_frame(self):
        for entry in self.entries:
            entry.grid_forget()

    def delete_param(self, i):
        self.clear_frame()
        del self.entries[i]
        self.build_frame()

    def get_delete_callback(self, i):
        return lambda event: self.delete_param(i)

    def build_frame(self):
        for i, entry in enumerate(self.entries):
            entry.add_to_grid(i)
            entry.delete_widget.bind(
                "<ButtonPress-1>",
                self.get_delete_callback(i))

    def get_i_from_y(self, event):
        for i, entry in enumerate(self.entries):
            if entry.in_y(event):
                return i
        return -1

    def get_i_from_xy(self, event):
        for i, entry in enumerate(self.entries):
            if entry.contains_event(event):
                return i
        return -1

    def contains_event(self, event):
        return is_event_in_widget(event, self)

    def mouse_down(self, event):
        self.i_select = self.get_i_from_xy(event)
        if self.i_select == -1:
            return
        entry = self.entries[self.i_select]
        entry.num_widget.configure(background='#FF9999')
        entry.fname_widget.configure(background='#FF9999')

    def mouse_up(self, event):
        if self.i_select == -1:
            return
        entry = self.entries[self.i_select]
        entry.num_widget.configure(background='white')
        entry.fname_widget.configure(background='white')

    def mouse_drag(self, event):
        self.i_mouse_drag = self.get_i_from_y(event)
        if self.i_select == -1 or self.i_mouse_drag == -1:
            return
        if self.i_select == self.i_mouse_drag:
            return
        i, j = self.i_mouse_drag, self.i_select
        self.entries[i], self.entries[j] = self.entries[j], self.entries[i]
        self.clear_frame()
        self.build_frame()
        self.i_select = self.i_mouse_drag
        self.i_mouse_drag = -1

    def get(self):
        return [(e.fname, e.label_stringvar.get()) for e in self.entries]


class HyperlinkManager:

    """
    Manager of links that can be clicked in a text object.
    Maintains linkages between mouse interactions and commands.
    From http://effbot.org/zone/tkinter-text-hyperlink.htm
    """

    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add_new_link(self, action):
        "Returns tag for link to use in tk.Text widget"
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return


class LabeledEntry(tk.Frame):

    """
    Creates a frame that holds a label, a button and a text entry
    in a row. The button is used to load a filename or directory.
    """

    def __init__(
            self, parent, text, entry_text='',
            load_file_text=None,
            load_dir_text=None):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.grid()

        self.stringvar = tk.StringVar()
        self.stringvar.set(entry_text)

        self.label = tk.Label(self, text=text)
        i_column = 0
        self.label.grid(column=i_column, row=0)

        i_column += 1
        self.button = None
        if load_file_text:
            self.button = tk.Button(
                self, text=load_file_text, command=self.load_file)
            self.button.grid(column=i_column, row=0)
            i_column += 1
        if load_dir_text:
            self.button = tk.Button(
                self, text=load_dir_text, command=self.load_dir)
            self.button.grid(column=i_column, row=0)
            i_column += 1

        self.entry = tk.Entry(self, textvariable=self.stringvar)
        self.entry.grid(column=i_column, row=0)

    def load_file(self):
        fname = tkFileDialog.askopenfilename()
        self.stringvar.set(fname)

    def load_dir(self):
        fname = tkFileDialog.askdirectory()
        self.stringvar.set(fname)

    def get(self):
        return self.stringvar.get()


def fix_list(tcl_list):
    """
    fix for Windows where askopenfilenames fails to format the list
    """
    if isinstance(tcl_list, list) or isinstance(tcl_list, tuple):
        return tcl_list
    regex = r""" 
    {.*?}   # text found in brackets
    | \S+   # or any non-white-space characters 
  """
    tokens = re.findall(regex, tcl_list, re.X)
    # remove '{' from start and '}' from end of string
    return [re.sub("^{|}$", "", i) for i in tokens]


def askopenfilenames(*args, **kwargs):
    """
    Wrap the askopenfilenames dialog to fix the fname list return
    for Windows, which returns a formatted string, not a list.
    """
    fnames = tkFileDialog.askopenfilenames(*args, **kwargs)
    return fix_list(fnames)


def exit():
    """
    Convenience function to close Tkinter.
    """
    tk.Tk().quit()


class Form(tk.Tk):

    """
    A Form to collect parameters for running scripts in Python.

    Parameters are created in the initialization with:
    - push_labeled_param
    - push_checkbox_param
    - push_radio_param
    - push_file_list_param

    `get_params` will return the current set parameters, this is normally
    set as a callback from the submit button.

    For decorative purposes, use:
    - push_text
    - push_spacer

    A submit button to trigger the form

    Other buttons can be added with Pythonic callbacks:
    - push_button

    Creates a hyperlinkManager instance to allow links to appear in the form.

    Keeps track of child mouse_widgets to send mouse events.

    Creates an (optional) text output area to pipe messages from the running
    of the script.
    """

    def __init__(self, title='', width=700, height=800, parent=None):
        self.parent = parent
        tk.Tk.__init__(self, parent)

        if width < 0:
            width = self.winfo_screenwidth() + width
        self.width = width

        if height < 0:
            height = self.winfo_screenheight() + height
        self.height = height

        self.geometry("%dx%d" % (width, height))
        if title:
            self.title(title)

        self.vscroll_frame = VerticalScrolledFrame(self)
        self.vscroll_frame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.interior = self.vscroll_frame.interior
        self.interior.configure(bd=30)
        self.i_row_interior = 0

        self.output = None
        self.output_str = ''
        self.output_link_manager = None

        self.param_entries = collections.OrderedDict()

        self.mouse_widgets = []
        self.bind('<Button-1>', self.mouse_down)
        self.bind('<B1-Motion>', self.mouse_drag)
        self.bind('<ButtonRelease-1>', self.mouse_up)

    def mouse_down(self, event):
        for widget in reversed(self.mouse_widgets):
            if widget.contains_event(event):
                widget.mouse_down(event)

    def mouse_up(self, event):
        for widget in reversed(self.mouse_widgets):
            if widget.contains_event(event):
                widget.mouse_up(event)

    def mouse_drag(self, event):
        for widget in reversed(self.mouse_widgets):
            if widget.contains_event(event):
                widget.mouse_drag(event)

    def push_row(self, widget):
        self.i_row_interior += 1
        widget.grid(row=self.i_row_interior, column=0, sticky=tk.W)

    def push_text(self, text, fontsize=12):
        label = tk.Label(
            self.interior, font=('defaultFont', fontsize), text=text)
        self.push_row(label)

    def push_spacer(self, height=1):
        label = tk.Label(self.interior, height=height)
        self.push_row(label)

    def push_line(self, width=500, height=1, color="#999999"):
        canvas = tk.Canvas(self.interior, width=width, height=height, bg=color)
        self.push_row(canvas)

    def push_button(self, text, command_fn):
        button = tk.Button(self.interior, text=text, command=command_fn)
        self.push_row(button)

    def push_labeled_param(
            self, param_id, text, entry_text='',
            load_file_text=None, load_dir_text=None):
        entry = LabeledEntry(
            self.interior, text, entry_text, load_file_text=load_file_text,
            load_dir_text=load_dir_text)
        self.push_row(entry)
        self.param_entries[param_id] = entry

    def push_file_list_param(
            self, param_id, load_file_text, is_label=True):
        file_list = ReorderableLabeledList(self.interior)

        def load_file():
            fnames = askopenfilenames(title=load_file_text)
            for fname in fnames:
                if is_label:
                    label = os.path.basename(fname)
                else:
                    label = None
                file_list.add_entry_label(fname, label)
        load_files_button = tk.Button(
            self.interior, text=load_file_text, command=load_file)
        self.push_row(load_files_button)

        self.push_row(file_list)
        self.mouse_widgets.append(file_list)
        self.param_entries[param_id] = file_list

    def push_dir_list_param(
            self, param_id, load_dir_text, is_label=True):
        file_list = ReorderableLabeledList(self.interior)

        def load_dir():
            the_dir = tkFileDialog.askdirectory(title=load_dir_text)
            if is_label:
                label = os.path.basename(the_dir)
            else:
                label = None
            file_list.add_entry_label(the_dir, label)
        load_dir_button = tk.Button(
            self.interior, text=load_dir_text, command=load_dir)
        self.push_row(load_dir_button)

        self.push_row(file_list)
        self.mouse_widgets.append(file_list)
        self.param_entries[param_id] = file_list

    def push_checkbox_param(self, param_id, text, init_val='1'):
        int_var = tk.IntVar()
        int_var.set(init_val)
        check_button = tk.Checkbutton(
            self.interior, text=text, variable=int_var)
        self.push_row(check_button)
        self.param_entries[param_id] = int_var

    def push_radio_param(self, param_id, text_list, init_val=0):
        int_var = tk.IntVar()
        buttons = []
        for i, text in enumerate(text_list):
            val = i
            button = tk.Radiobutton(
                self.interior, text=text, value=val, variable=int_var)
            buttons.append(button)
        int_var.set(str(init_val))
        for button in buttons:
            self.push_row(button)
        self.param_entries[param_id] = int_var

    def get_params(self):
        params = collections.OrderedDict()
        for param_id, entry in self.param_entries.items():
            params[param_id] = entry.get()
        return params

    def push_output(self):
        if self.output is not None:
            raise Error('Error: push_output has been called more than once!')
        self.output = tk.Text(self.interior, state=tk.DISABLED)
        self.output_link_manager = HyperlinkManager(self.output)
        self.push_row(self.output)

    def clear_output(self):
        if self.output is None:
            raise Exception("Output not initialized in Form")
        self.output.configure(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output_str = ""
        self.update()
        self.output.configure(state=tk.DISABLED)

    def print_output(self, s, cmd_fn=None):
        if self.output is None:
            raise Exception("Output not initialized in Form")
        self.output.configure(state=tk.NORMAL)
        if cmd_fn is not None:
            link_tag = self.output_link_manager.add_new_link(cmd_fn)
            self.output.insert(tk.INSERT, s, link_tag)
        else:
            self.output.insert(tk.INSERT, s)
        self.output_str += s
        self.update()
        self.output.configure(state=tk.DISABLED)

    def run(self, params):
        "Dummy method to be overriden/replaced."
        pass

    def print_exception(self):
        if self.output is not None:
            s = "\nTHERE WERE ERROR(S) IN PROCESSING THE PYTHON.\n"
            s += "Specific error described in the last line:\n\n"
            s += traceback.format_exc()
            s += "\n"
            self.print_output(s)

    def submit(self):
        if self.output is not None:
            self.clear_output()
        try:
            params = self.get_params()
            self.run(params)
        except:
            self.print_exception()

    def push_submit(self):
        self.push_button('submit', self.submit)
