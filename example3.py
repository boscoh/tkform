#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import os
import json
import webbrowser

import Tkinter as tk
import tkFileDialog

import tkform


class ExampleForm(tkform.Form):

    """
    Example tkform with Reorderable List
    """

    def __init__(self, width=700, height=800, parent=None):
        tkform.Form.__init__(self, parent, width, height)

        self.title('Reorderable List Example')
        self.push_text("Reorderable List Example", 30)
        self.push_line()
        self.push_spacer()
        self.push_text(u"Drag \u2630 to reorder filenames")
        self.push_custom_loader('filenames_and_labels', '+ files')
        self.push_spacer(2)
        self.push_text("Output", 16)
        self.push_line()
        self.push_submit()
        self.push_output()

    def push_custom_loader(self, param_id, button_text):
        self.reorderable_list = tkform.ReorderableList(self.interior)
        self.datas = []

        def load_peptagram():
            fnames = tkFileDialog.askopenfilenames(title=button_text)
            try:
                self.print_output('Loading %d filenames... ' % len(fnames))
            except:
                self.print_exception()

            for fname in fnames:
                basename = os.path.basename(fname)
                self.reorderable_list.add_entry_label(fname, basename)

        load_button = tk.Button(
            self.interior,
            text=button_text,
            command=load_peptagram)
        self.push_row(load_button)

        self.push_row(self.reorderable_list)
        self.mouse_widgets.append(self.reorderable_list)
        self.param_entries[param_id] = self.reorderable_list

    def run(self, params):

        self.print_output('\nForm parameters:\n')

        self.print_output(json.dumps(params, indent=2))
        self.print_output('\n\n')


ExampleForm(800, -150).mainloop()
