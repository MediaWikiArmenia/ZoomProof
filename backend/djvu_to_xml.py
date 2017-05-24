import subprocess
import html

#we remove the named xml entities from the lookup here,
#so that they will be untouched when unescaping xml later on
del html.entities.html5['gt;']
del html.entities.html5['lt;']
del html.entities.html5['amp;']
del html.entities.html5['gt']
del html.entities.html5['lt']
del html.entities.html5['amp']

def convert_from_file(filepath, page):
  """read the given page from the djvu file filename using unix tool 'djvutoxml'"""
  #define the command we want to run and its arguments in order
  command_line_args = ['djvutoxml', '{}'.format(filepath), '--page', '{}'.format(page)]
  #run the command, store its output converted from byte array to utf-8 python3 string
  command_output_str = subprocess.check_output(command_line_args).decode('utf-8')
  #converting HTML entities in the str to the corresponding unicode characters
  #e.g. '&#10;' -> '\n'
  output_str_unescaped = html.unescape(command_output_str)
  return output_str_unescaped

#python >=3.5 version of this:
#command_output = subprocess.run(command_line_args, stdout=subprocess.PIPE)
#output_str = command_output.stdout.decode('utf-8')
