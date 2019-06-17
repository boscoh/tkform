

# tkform

a cross-platform form-based GUI to run command-line utilities using standard Python.

![](./screenshot.png)

## Quick Start

### Installation instructions

To install tkform:

     pip install tkform

Or download and unzip:

&nbsp; &nbsp; &nbsp;  [tkform-master.zip](https://github.com/boscoh/tkform/archive/master.zip)

Then install:

    > python setup.py install

### Examples

1. `python example1.py` - loads a filename and sends it a webpage
2. `python example2.py` - is more involved which involve displaying output
3. `python example3.py` - shows how to customize reoderable lists

### Making a Quick-and-Dirty Form

Here's how to make a simple form (this is similar to `example1.py`). 

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
    form.push_file_list_param('files_and_labels', '+ files')

Then add the crucial submit button:

    form.push_submit()

The submit button will trigger the `run` method, so let's  override it with our own: 

    form.run = my_run

Then go:

    form.mainloop()

## What is it?

You want to wrap a simple GUI around a command-line utility. As the idea of a GUI is to make it easy for end-users, you probably also want it to be:

1. cross-platform - useful for as many end-users as possible
2. open files with native file-chooser - familiarity is important for usability
3. easy to install - which is as important as being easy-to-use

No existing solution quite satisifiy all three requirements. One solution is [`gooey`](https://github.com/chriskiehl/Gooey), which cleverly wraps a cross-platform `wxPython` GUI around Python scripts.  But sadly, it requires `wxPython`, which is difficult to install for end-users. You either need to match binary versions of `wxPython` to your Python package, or install a C compiler ecosystem. 

Another solution is to run a local webbrowser. This is powerful except for one hobbling limitation. Due to the security model of the webbrowser, your  native open-file dialog will never give you full pathnames to your scripts. This severely constrains your scripts.

Instead, we have built `tkform` which provides a base for building a simple GUI around Python scripts that is designed for a non-technical end-user. It is designed against `tkinter`, which is bundled with Python. Your user has only to install Python, which is easy. `tkinter` provides native file-choosers, and as it's all in Python, your GUI will be cross-platform.

## How does it work?

Typically, you will want to sub-class `tkform.Form` to use all the features: callback buttons, integrated text output, filename processing etc. The following is similar to the example `example2.py`.

### 1. Subclassing your own Form

First import the library:

    import tkform

Then subclass it with your ow:

    class MyForm(tkform.Form):
        def __init__(self):
             tkform.Form.__init__(self, title, width, height)

The window will appear in the top-left of the screen. The `width` and the `height` define the size of the window. You can use negative values which will set, for the `width`, to the width of the screen subtracted by the negative value. Similarly for `height`. If you want to maximize the height of the window, a value of -150 seems to work across all platforms.

### 2. Creating the form - the grid model 

The way the form is built is with a vertical grid layout, similar to how many HTML forms are laid out. Internally, a tkinter grid is used and all widgets are left-aligned. A vertical scroll-bar will be applied that lets your form grow.

The form will return a dictionary where each key/value pair is determined by what objects are pushed onto the form. The key/value pairs are determined by what paramaters you push onto the form in the initialization via the `push*_param` methods.

_Parameters_.  Available param types are defined by these methods:

- multiple file list loader

        push_file_list_param(param_id, load_file_text, is_label=True)

    This creates a button, which, when clicked, triggers an open file dialog box to chose multiple files. Files chosen here will pop up in a table of files. This may include an optional label for each file as determined by the `is_label` flag. This table of files can be reordered, or removed. When the submit button is pressed, the widget will return a list of tuples in `params` of the run function. In the tuple, the first element is the filename, with an optional second element corresponding to the label.

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
      # Do your thing with params or run an external function

At the end of `run` you have a choice:

1. you can exit the form with `tkform.exit()`
2. or the window stays open and the user can submit again _ad nauseum_.

A nice thing is that if you've carried out some external action, say opening a web-page, that will stay open if you've closed the form.

When `run` is called, it is wrapped in a try/except clause to catch errors that are optionally sent to the ouptut widget, which will be discussed next.


### 4. Handling output (optional)

The form provides an (optional) output widget to provide feedback to the user within the form itself. The output area is registered on the form via the method with an optional width parameter:

    self.push_output(width=50)

During the processing in `run`, you can add text:

    self.print_output('Processing...\n')

This `print_output` does not include an implicit carriage-return, this allows you to display progressive text ouptut. The form will automatically increase in size to display the output. You can flush the output at different stages of the processing with:

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

## Customizing Forms

If you want to customize your own widgets then have a look at the widgets instantiated in the `Form` class.

Any `tkinter` widgets can be displayed in the form by `self.push_row(my_tkinter_widget)`. This could include buttons that trigger functions or any other kind of actions.

To add key-value pairs to the `params` that is generated when the submit button is pressed, you must add an object to the `self.param_entries` dictionary:
	
    self.param_entries[param_id] = entry

The value `entry` must have a `get` method that returns a json compatible data structure (lists, dictionaries, strings and numbers).

## Customizing Reorderable Lists

One feature that `tkform` provides is the ability to preload a list of items before the `submit` button is pressed. An example is the widget generated with the `push_file_list_param` method. This list can be reordered, or truncated, and labels can be attached to them.

To generated your own editable list, you can create your own widgets based on the `ReorderableList` class. On initialization, you must instantiate an `ReorderableList` on the page. Then you create a button that that triggers an action (say an open file dialog), which will populate your `ReorderableList`. This shows up on the page instantaneously. As well, you must provide an object to return in the `self.param_entries` dictionary. The `ReorderableList` serves this function, with its default `get` method. But you can certainly substitute your own. 

Anyway, check out  `example3.py` to see how a customized `ReorderableList` is built.

## Processing the submit button

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

## Making scripts clickable for the End User
        
It's useful to wrap the python script with a unix shell script or a Windows batch file so that the end-user can double-click in the file manager.

For instance we can make for `example1.py`, a batch file `example1.bat`:

     python tkform1_ex1.py %1 %2 %3
     
And in *nix, we ca make `example1.command`:

    DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    cd $DIR
    python example1.py $*example
   
Make sure the file is `chmod +c example1.command`. The extension of .command allows the MacOS finder to allow double-clicking.  Indeed, to close the window that pops after the form is closed, you need to also add, for MacOS:

    if [ "$(uname)" == "Darwin" ]; then
        echo -n -e "\033]0;example1.command\007"
        osascript -e 'tell application "Terminal" to close (every window whose name contains "example1.command")' &
    fi

## Changelog

1.0 (June 2015)

- ReorderableList abstraction
- Output auto-sizing

&copy; Bosco K ho.

