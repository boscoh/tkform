

# tkform

`tkform` provides a simple form-based GUI interface to run your Python scripts.

It's super easy to install because it only requires tkinter, which comes standard with all Python distributions.

It's particular useful for generating file-based displays because it includes a custom-made reorderable file-list widget.

## Quick Start

### Installation instructions

To install tkform, simply clone the project to your local directory

    > git clone http://github.com/boscoh/tkform

And run setup.py

    > python setup.py install

Then run the examples

    > python tkform_ex1.py
    > python tkform_ex2.py

### Making a Quick-and-Dirty Form

The model follows a typical web-based form: type in a bunch of parameters and you get a dictionary that can be slurped into your scripts.

The simplest example is in `tkform_ex1.py`. It doesn't even bother handling the processing output.

The `Form` object can be instantiated and populated on the fly. This produces a quick-and-dirty GUI as you simply plug in your own function when the `submit` button is clicked.

## What is it for?

It's for building a simple GUI for your Python scripts with a minimum of fuss. This is to let your users run your scripts without dealing with the command-line or config files.

tkform is designed to be really easy to install - it has no dependency apart from the default Python package. Other toolkits - wxPython and can be ... problematic.

tkinter is pretty good now, where the file open dialogs are standard to each operating system. Not so much for the widget set, but this is pretty basic stuff here.


## How to use

The Form object is cobbled together from various widgets in the tkinter ecosystem. It's inspired by HTML5-based forms where you define a bunch of parameters with a submit button. Once clicked, a dictionary will be generated and sent to the `self.run(params)` method in the Form object.

### Subclassing your own Form

To use, simply subclass the Form object. Preparation consists of 2 parts:

1. __init__ function where the form is generated
2. overriding the `run(params)` hook with progress output and hyperlinks

### Initializing the form

This approach is the most straightforward. You initialize the object by registering a list of paramters with an associated identifier:

- file-list or directory-list

    `push_filelist_param('file_list', 'go for it', '+ file')`

- check boxes:

    `push_checkbox_param`

- radio buttons

    `push_radio_param`

- text parameter, which could be selected as a file or directory

    `push_labeled_param`

Somewhere in the form, you need to put a submit button:

    push_submit()

And (optionally) an output area:

    push_output()

### Form Decorations

Of course you need other things to make a ussable form.

Text at different sizes:

    push_text

Lines to divide sections:

    push_line

And sometimes, just some white-space:

    push_space


### Extra buttons

Sometimes you might want to trigger some action BEFORE the form is submitted. Just add a button and throw in a a call-back function:

    self.push_button('text', lambda: pass)

### Setting up processing

Then when the submit button is clicked, the Form object collects the parameters and sends this as an OrderedDict into the hook:

    self.run(params):
      pass

You can override this function where you handle the params.

But more importantly, if you have set up the output, you can now send progress reports to this output



During the run function, you can output to a special text-area in the Form, which also captures exceptions in your function.

When you scripts are finished, you can create hyperlinks that will take the user to the results, and exit out of the Form.

Why do you want to subclass? 

Mainly to get access to the built in output area. This is initialized with the optional `push_output()` in the constructor.

During the processing in `run`, you can clear the output:

    self.clear_output()

You can add text:

    self.print_output('Processing...\n')

You can add links:

    self.print_output('You can now click ')

    def show_results():
      # do someting

    self.print_output('here', show_results)


### End of Processing

When overriding `run`, if you want the program to quit on success, you must explicitly close `tkinter` using the provided function

    tkform.exit()

&copy; 2014, Bosco K ho.

