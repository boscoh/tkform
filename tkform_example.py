#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import glob
import os
import webbrowser
import tkform


class ExampleForm(tkform.Form):
  """
  Application window for Tkinter.
  """ 
  def __init__(self, width=700, height=800, parent=None):
    tkform.Form.__init__(self, parent, width, height)

    # set the title of the form window
    self.title('tkform Example')

    # add text
    self.push_text("tkform Example", 30)
    
    # add space between rows
    self.push_spacer()
    # add dividing line
    self.push_line()

    # add a file loading list object
    self.push_text("Example of a file list loader:", 16)
    self.push_file_list_param(
        'files_and_labels',
        load_file_text='+ add files')

    self.push_spacer()
    self.push_line()

    self.push_text("Example of a file directory loader:", 16)
    self.push_file_list_param(
        'dirs_and_labels',
        load_dir_text='+ add directory')

    self.push_spacer()
    self.push_line()

    # some text labels
    self.push_text("Example of labeled (file/directory) entries:", 16)
    self.push_labeled_param(
        'param1', 'enter a number for param1', '1')
    self.push_labeled_param(
        'param2', 'enter file2', 'default_file', load_file_text='select')
    self.push_labeled_param(
        'param3', 'enter dir3', 'default_dir', load_dir_text='select')

    self.push_spacer()
    self.push_line()

    self.push_text("Example of Checkbox:", 16)
    self.push_checkbox_param('include_msms', 'include MS/MS')

    self.push_spacer()
    self.push_line()

    self.push_text("Example of Radio Button:", 16)
    self.push_radio_param(
        'radio_param',
        ['choice 0', 
         'choice 1', 
         'choice 2', 
         'choice 3'])

    self.push_spacer()
    self.push_line()

    self.push_text("Click here to run script", 16)
    self.push_submit()

    self.push_spacer()
    self.push_line()

    self.push_text("Output", 16)

    # Must register the output if you want to
    # display output during the execution of your commands
    self.push_output()


  def run(self, params):
    """
    Override the command that is run when "submit" is
    pressed.
    """

    self.clear_output()

    self.print_output('Gathering parameters:\n')
    params = self.get_params()
    self.print_output('{\n')
    for key in params:
      self.print_output('  %s: %s,\n' % (str(key), str(params[key])))
    self.print_output('}\n')
    self.print_output('Executing command...\n')

    def cmd_fn():
      pass

    self.print_output('this is a link', cmd_fn)



if __name__ == "__main__":
    form = ExampleForm(700, 900)
    form.mainloop()




