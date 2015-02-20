

# tkform

`tkform` wraps an elegant form-based GUI around Python scripts using only standard Python.

### Screenshot

## Quick Start

### Installation instructions

To install tkform, simply clone the project to your local directory

    > git clone http://github.com/boscoh/tkform

And run setup.py

    > python setup.py install

There are two examples provided. 

The first example loads a filename and sends it a webpage:

    > python tkform_ex1.py

The second example shows is more involved which involve displaying output:

    > python tkform_ex2.py

### Making a Quick-and-Dirty Form

Here's how to make a simple form (this is similar to `tkform_ex1.py`). 

First some house-keeping:

    import tkform, os, webbrowser

Let's define a function that receives a `params` dictionary:

    def my_run(params):
        open('index.html', 'w').write(params['files_and_labels'])
        webbrowser.open('file://' + os.path.abspath('index.html')

Notice the function expects a key of `files_and_labels` in `params` .

A quick-and-dirty form can be instantiated and populated on the fly. :

    form = tkform.Form('Window title of form', 700, 900)

Let's populate the form with a header, file/dir list parameter:

    form.push_text(title, 20)
    form.push_file_list_param('files_and_labels', load_file_text='+ files')

Then add the crucial submit button:

    form.push_submit()

The submit button will trigger the `run` method, so let's  override it with our own: 

    form.run = my_run

Then go:

    form.mainloop()

## What is it?

You want to wrap a simple GUI around a command-line utility or a Python script. For usability, these properties are essential:

1. cross-platform
2. native platform file-&-directory chooser
3. easy installation for end-users

Now there are some great solutions out there, but none of them quite hit the sweet spot. One possible solution is [`gooey`](https://github.com/chriskiehl/Gooey), a clever cross-platform solution that wraps a `wxPython` GUI around Python scripts. 

The downfall is the installation of `wxPython`. Go to the [download page](http://www.wxpython.org/download.php), and you'll see that there are packages for a confusing number of combinations of operating systems and versions of Python. You can't reliably install `wxPython` with `pip` as it is too brittle. Installing `wxPython` will simply frustrate most of your end-users. Similar problems plague other cross-platform toolkits.

Another solution is to run everything through a local webbrowser. I've done tons of webapps and building GUIs in the webbrowser is  powerful. However, there is one terrible limitation. Although webbrowsers provide a native open-file dialog, due to the intrinsic security model, the webbrowser will never let you pass the full pathname to the webserver. This severely limits the filenames you can use in your scripts.

Well it turns out standard Python provides `tkinter`, with which you could build a cross-platform GUI with native open-file dialogs. The problem is that `tkinter` is fugly and temperamental. `tkform` is a library that cobbles together tkinter objects into a usable form to wrap command-line scripts.

## How does it work?

Typically, you will want to sub-class `tkform.Form` to use all the features: callback buttons, integrated text output, filename processing etc. The following is similar to the example `tkform_ex2.py`.

### 1. Subclassing your own Form

First import the library:

    import tkform

Then subclass it with your ow:

    class MyForm(tkform.Form):
        def __init__(self):
             tkform.Form.__init__(self, title, width, height)

The window will appear in the top-left of the screen. The `width` and the `height` define the size of the window. You can use negative values which will set, for the `width`, to the width of the screen subtracted by the negative value. Similarly for `height`.

### 2. Creating the form - the grid model 

The way the form is built is with a vertical grid layout, similar to how many HTML forms are laid out. Internally, a tkinter grid is used and all widgets are left-aligned. A vertical scroll-bar will be applied that lets your form grow.

The form will return a dictionary where each key/value pair is determined by what objects are pushed onto the form. The key/value pairs are determined by what paramaters you push onto the form in the initialization via the `push*_param` methods.

_Parameters_.  Available param types are defined by these methods:

- multiple file list loader

        push_file_list_param(param_id, load_file_text, is_label=True)

    This creates a button, which, when clicked, triggers an open file dialog box to chose multiple files. Files chosen here will pop up in a table of files. This table of files can be reordered. The file entries can be given an optional label as determined by the `is_label` flag. As well, the file entries can be removed. 

- directory list loader

        push_file_dir_param(param_id, load_dir_text, is_label=True)

    This is similar to `push_file_list_param` above except it opens directories. Unfortunately tkinter only allows you to select one directory at a time.

- check box

        push_checkbox_param(param_id, text, init_val='1')

    This creates a checkbox that will return a string `1` if selected, and `0` otherwise.

- radio button

         push_radio_param(param_id, text_list, init_val=0)

     This creates a radio button from a list of options determined by a list of strings in `text_list`. The return value is an integer that refers to entries in `text_list`.
- text parameter, optionally as single file/directory

         push_labeled_param(param_id, text, entry_text='', load_file_text=None, load_dir_text=None)

     This creates a text entry that is passed to the `params` dictionary. This is also used for loading a single filename or a single directory. If `load_file_text` is not empty, a button will be created with that label text, which will trigger a file-open dialog box. Similarly for `load_dir_text`.

_Decorators_. Of course you need other things to make the form readable:

- text at different sizes: `push_text(text, fontsize=12)`
- lines to divide sections: `push_line(width=500, height=1, color="#999999")`
- and white-space: `push_spacer(self, height=1)`

_Extra buttons and callbacks_. 

- Although `tkform` is conceived around a single submit button at the end, sometimes you might want to trigger some action before the form is submitted. To do this, first define the action you want to take:

        def callback():
           # do something

    Then push the button onto the form, and link the callback:

        self.push_button('text', callback)

### 3. Submitting the job

Most importantly you need to add a submit button, probably at the bottom of the form:

    push_submit()

When the submit button is clicked, `tkform` will extract the parameters from all the widgets with `*_param*`, and put them in the `params` dictionary. This will be sent to the  `self.run(params)` method. 

In the `Form` class, this is a dummy method that needs to be overriden:

    self.run(params):
      # Do your thing with params or run an an external function

At the end of `run` you have a choice:

1. you can exit the form with `tkform.exit()`
2. or the window stays open and the user can submit again _ad nauseum_.

A nice thing is that if you've carried out some external action, say opening a web-page, that will stay open if you've closed the form.

When `run` is called, it is wrapped in a try/except clause to catch errors that are optionally sent to the ouptut widget, which will be discussed next.


### 4. Handling output (optional)

The form provides an (optional) output widget to provide feedback to the user within the form itself. The output area is registered on the form via the method:

    self.push_output()

During the processing in `run`, you can add text:

    self.print_output('Processing...\n')

This `print_output` does not include an implicit carriage-return, this allows you to display progressive text ouptut.

You can clear the output if different stages of the processing have successfully completed:

    self.clear_output()

The `print_output` also has simple hyperlink facility. Simply adding a callback function as a second parameter will turn the text into a hyperlink. 

For instance, if you have written results to a webpage `/user/result/index.html`, you can define a display-results callback:

    import webbrowser
    def show_results():
      webbrowser.open('file://user/result.html')

This will produce a hyperlink that will open the local web-page to your results:
 
    self.print_output('results page', show_results)

### 5. Execute the form

Instantiate your form:

    form = Myform()

And run it:

    form.mainloop()

## Integrating the main processing function

It's very easy to work the GUI as optional feature within a command-line Python script. If you parameterise the main function in the form:

     def main_processing(params, print_output=std.write.out):
         # do something with params
         print_output('sucess...')

This takes a params dictionary, and for output, it writes to the function print_output. This can be put in the `run` method of the form:

     class Myform(tkform.Form):
         ...
         def run(self, params):
             main_processing(params, self.output)

And `main_processing` lends itself to take in arguments from the command-line parameters.
        
It's useful to wrap the python script with a unix shell script or a Windows batch file so that the end-user can double-click in the file manager.

&copy; 2015, Bosco K ho.

