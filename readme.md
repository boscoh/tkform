

# tkform

`tkform` provides a simple interface to tkinter to provide an HTML-inspired form-like GUI to run Python scripts.

It's cobbled together from a couple of useful widgets in the tkinter ecosystem

- a growable page with vertical scrollbar
- a custom reorderable file-list
- simple loading of form parameters
- clean hook to grab parameters & run scripts
- ouptut area for progress reports

It's mean to create simple GUI interfaces for your scripts that's easy to distribute and install for your users.

## Custom reorderable file-list

This is a useful widget to slurp in list of files. 

It is reorderable which is really important when generating tables and images.

## Target Distribution

This is similar to [`Gooey`](https://github.com/chriskiehl/Gooey), but I've had serious problems installing `Gooey`'s dependency wxWidgets. 

In contrast, `tkform` has no dependencies but vanilla Python, making distribution so much easier.

## Installation

The project is stored at [github](http://github.com/boscoh/tkform).

## Usage

It's designed to be subclassed and built with your own.

Check out the example file `tkform_example.py` included in the package.

    