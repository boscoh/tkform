#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import tkform


def make_index(params):
    import os, json, webbrowser
    fname = os.path.abspath('tkform_ex2.html')
    template = "<h1>Tkform Params to JSON</h1><pre>%s</pre>"
    open(fname, 'w').write(template % json.dumps(params, indent=2))
    webbrowser.open('file://'+fname)
    tkform.exit()


form = tkform.Form(None, 700, 900)
form.push_text("tkform example with filelist", 20)
form.push_file_list_param('files_and_labels', load_file_text='+ files')
form.push_submit()
form.run = make_index
form.mainloop()




