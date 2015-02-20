

# tkform

`tkform` provides a simple form-based GUI interface to run your Python scripts.

It's super easy to install because it only requires tkinter, which comes standard with all Python distributions.

It's particular useful for generating file-based displays because it includes a custom-made reorderable file-list widget.

### Screenshot

## Quick Start

### Installation instructions

To install tkform, simply clone the project to your local directory

    > git clone http://github.com/boscoh/tkform

And run setup.py

    > python setup.py install

There are two examples provided. The first just picks a filename and then opens a web-page with the full filename:

    > python tkform_ex1.py

The second example shows how more complicated parameters are processed:

    > python tkform_ex2.py

### Making a Quick-and-Dirty Form

Let's go through the process of writing a tkform, similarly to `tkform_ex1.py`. First let's do some house-keeping:

    import tkform
    import os, webbrowser

Let's define a function that receives a dictionary of parameters to use:

    def my_run(params):
        open('index.html', 'w').write(params['files_and_labels'])
        webbrowser.open('file://' + os.path.abspath('index.html')

Notice the function expects a key of `files_and_labels` in the `params` dictionary.

The `Form` object can be instantiated and populated on the fly. This produces a quick-and-dirty GUI as you simply plug in your own function when the `submit` button is clicked. Essentially it is this:

    form = tkform.Form('Quick example', 700, 900)

Let's populate the form with a header, file/dir list parameter:

    form.push_text(title, 20)
    form.push_file_list_param('files_and_labels', load_file_text='+ files')

Then add the crucial submit button:

    form.push_submit()

The submit button when pressed will trigger the `run` method, let's override it with our own: 

    form.run = my_run

Then go:

    form.mainloop()

## What is it for?

_The Problem_. You want to wrap a simple GUI around a command-line utility or a Python script. For usability, these properties are essential:

1. cross-platform
2. native platform file-&-directory chooser
3. easy installation for end-users
 
Now there are some great solutions out there, but none of them hit the sweet spot. I'll discuss two.

First, a great cross-platform example is `gooey`, a clever wrapper around Python scripts that bootstraps the `argparse` library to autogenerate a `wxPython` GUI. It's fantastic. 

The downfall is the installation. Installing `wxPython` is tricky for users who are not expert in Python. Go to the download page, and you'll see that there are packages for different versions of operating systems and Python interpreters. As the `wxPython` package is too brittle to be reliably installable with `pip`, getting it working takes a lot of fiddly experimentation, enough to frustrate most end-users. 

Installation problems plague other cross-platform toolkits such as `qt` and `gtk`.

Second, another solution is to run everything through a webbrowser via a local Python webserver. I've done tons of webapps and building GUIs in the webbrowser is very powerful. 

However, there is one terrible limitation to this method. Although you can open files using a native open-file dialog, due to the intrinsic security model of the webbrowser, the webbrowser will never let you pass the full pathname of an open dialog to the local webserver. This severely limits the filenames you can use in your command-line binaries.

_The solution_. Installing Python is now pretty straightforward, if not even included in your operating system. Well it turns out that a cross-platform widget library comes with every single install of Python: `tkinker`. 

tkinter has file and directory dialogs that are native. And it's dead easy to wrap command-line binaries with Python. The only problem is that tkinter is a fugly toolkit.

`tkform` attempt to cobble together tkinter into a nice GUI that can easily wrap a command-line utility in Python. `tkform` overrides a lot of the display defaults in `tkinter` and imposes a web-form inspired look-and-feel. 

## How to use

More typically, you will want to sub-class `tkform.Form` to use all the features: callback buttons, integrated text output, filename processing etc. The following is similary to `tkform_ex2.py`.

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

Thus available param types are defined by these methods:

#### Parameter: multiple file/directory list loader

    `push_file_list_param(param_id, load_file_text='', load_dir_text='', is_label=True)`

This creates a button, which, when clicked, triggers an open file or an open directory dialog box. Files/directories chosen here will pop up in a table of files. This table of files can be reordered, the file entries can be given an optional label as determined by the `is_label` flag, and the file entries can be removed. Depending on whether `load_file_text` or `load_dir_text` has a string, 

   - param_id is the eventual `params` key
   - `load_file_text` is the text of the button label
   - `load_dir_text` is the text of the button label
   - `is_label` is a flag that determines whether a chosen file gets an optional label

####  Parameter: check box

    `push_checkbox_param(param_id, text, init_val='1')`

This creates a checkbox that will return a string `1` if selected, and `0` otherwise.

####  Parameter: radio button

    `push_radio_param(param_id, text_list, init_val=0)`

This creates a radio button from a list of options determined by a list of strings in `text_list`. The return value is an integer that refers to entries in `text_list`.

####  Parameter: text parameter, optionally as single file/directory

    `push_labeled_param(param_id, text, entry_text='', load_file_text=None, load_dir_text=None)`

This creates a text entry that is passed to the `params` dictionary. This is also used for loading a single filename or a single directory. If `load_file_text` is not empty, a button will be created with that label text, which will trigger a file-open dialog box. Similarly for `load_dir_text`.

#### Decorators

Of course you need other things to make the form readable:

- text at different sizes: `push_text(text, fontsize=12)`
- lines to divide sections: `push_line(width=500, height=1, color="#999999")`
- and white-space: `push_spacer(self, height=1)`

#### Extra buttons and callbacks

Although `tkform` is conceived around a single submit button at the end, sometimes you might want to trigger some action before the form is submitted. To do this, first define the action you want to take:

    def callback():
       # do something

Then push the button onto the form that links the action:

    self.push_button('text', callback)

### 3. Submitting the job

Most importantly you need to add a submit button, probably at the bottom of the form:

    push_submit()

When the submit button is clicked, `tkform` will extract the parameters from all the widgets with `*_param*`, and put them in the `params` dictionary. This will be sent to the  `self.run(params)` method. 

In the `Form` class, this is a dummy method that needs to be overriden:

    self.run(params):
      # Do your thing with params or run an an external function

At the end of `run` you have a choice:

1. you can kill the form with `tkform.exit()` and exit
2. or the window stays open and the user can submit again _ad nauseum_.

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


### Tips on writing the main processing function

It's very easy to work the GUI as optional feature within a command-line Python script. If you make the main script in the form:

     def main_processing(params, print_output=std.write.out):
         # do something with params
         print_output('sucess...')

This takes a params dictionary, and for output, it writes to the function print_output, which can be overriden:

     class Myform(tkform.Form):
         .
         .
         def run(self, params):
             main_processing(params, self.output)
        

&copy; 2015, Bosco K ho.

