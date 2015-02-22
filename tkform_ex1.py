#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import tkform


def make_index(params):
    """
    Our example run function that takes the params, converts
    it json, constructs a webpage, opens the webpage, and
    exits the original form.
    """
    import os
    import json
    import webbrowser
    fname = os.path.abspath('tkform_ex2.html')

    # make the webpage
    template = "<h1>Tkform Params to JSON</h1><pre>%s</pre>"
    open(fname, 'w').write(template % json.dumps(params, indent=2))

    # open the webpage
    webbrowser.open('file://' + fname)

    # to quit the form, must use this function
    tkform.exit()


# Create the form with title, width and height
title = "tkform example: bridge to webpage with json"
width, height = 700, 900
form = tkform.Form(title, width, height)

# Add some text
form.push_text(title, 20)

# And a loader for multiple files, registers a
# param with the dictionary key 'files_and_labels'
# this will be returned as params in the 'run' funtion
form.push_file_list_param('files_and_labels', '+ files')

# Must register the submit button
form.push_submit()

# When pushed the submit button will trigger `run`
# with parameters setup from above, replace with
# our own function that takes a params dictionary
form.run = make_index

# All set up? Trigger app.
form.mainloop()
