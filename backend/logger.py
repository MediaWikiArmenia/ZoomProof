import logging
import config

def setup_logger(name, filename, logging_level):
  """initializing a logger object"""
  #instantiating a new logger by calling 'getLogger' with a new name
  logger = logging.getLogger(name)
  logger.setLevel(logging_level)

  #logging format
  formatter = logging.Formatter('%(asctime)s : %(message)s')

  #write to a log file
  fileHandler = logging.FileHandler(filename, mode='a', encoding='utf-8')
  fileHandler.setFormatter(formatter)

  logger.addHandler(fileHandler)

def log_info(sha1, filename, page, info_msg):
  """log an info event"""
  log_info = logging.getLogger('log_info')
  if page:
    log_info.info("file: {} - {}, page: {}, {}".format(sha1, filename, page, info_msg))
  else:
    log_info.info("file: {} - {}, {}".format(sha1, filename, info_msg))

def log_error(sha1=None, filename=None, page=None, error_msg=""):
  """log an error event"""
  log_error = logging.getLogger('log_error')
  if sha1 is not None and filename is not None and page is not None:
    log_error.error("file: {} - {}, page: {}, {}".format(sha1, filename, page, error_msg))
  else:
    log_error.error("{}".format(error_msg))

def init_loggers():
  """initialize the loggers"""
  setup_logger('log_info', config.server['logdir']+'info.log', logging.INFO)
  setup_logger('log_error', config.server['logdir']+'error.log', logging.ERROR)

def read_log_n_latest(filename, n):
  """get the last n lines from logfile filename"""
  try:
    with open(filename) as logfile:
      n_latest = logfile.readlines()[-n:]
    return n_latest[::-1]
  except IOError:
    log_error = logging.getLogger('log_error')
    log_error.error("Can't open logfile {}".format(filename))

def get_latest_log_messages():
  """return the n latest (define in config) messages from the
     error log and the info log"""
  n = config.server['n_latest_log_messages']
  if n < 1:
    return [], []
  latest_errors = read_log_n_latest(config.server['logdir'] + 'error.log', n)
  latest_infos = read_log_n_latest(config.server['logdir'] + 'info.log', n)
  return latest_errors, latest_infos

init_loggers()
