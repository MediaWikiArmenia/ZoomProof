import subprocess

def convert_from_file(filepath, page):
  """read the given page from the pdf file filename using unix tool 'pdftotext'"""
  #define the command we want to run and its arguments in order
  command_line_args = [
      'pdftotext',
      '{}'.format(filepath),
      '-',                      #no output file specified means sending the output to stdout
      '-f', '{}'.format(page),  #first page to convert
      '-l', '{}'.format(page),  #last page to convert
      '-bbox',                  #output as xhtml with bounding box coordinates for every word
      '-layout'                 #try to enforce the output in text reading order
      ]
  #run the command, store its output converted from byte array to utf-8 python3 string
  command_output_str = subprocess.check_output(command_line_args).decode('utf-8')
  return command_output_str

#python >=3.5 version of this:
#command_output = subprocess.run(command_line_args, stdout=subprocess.PIPE)
#output_str = command_output.stdout.decode('utf-8')
