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
  fileHandler = logging.FileHandler(filename, mode='a')
  fileHandler.setFormatter(formatter)

  logger.addHandler(fileHandler)

def log_info(sha1, page, info_msg):
  """log an info event"""
  log_info = logging.getLogger('log_info')
  log_info.info("file: {}, page: {}, {}".format(sha1, page, info_msg))

def log_error(sha1, page, error_msg):
  """log an error event"""
  log_error = logging.getLogger('log_error')
  log_error.error("file: {}, page: {}, {}".format(sha1, page, error_msg))

def init_loggers():
  """initialize the loggers"""
  setup_logger('log_info', config.server['logdir']+'info.log', logging.INFO)
  setup_logger('log_error', config.server['logdir']+'error.log', logging.ERROR)
