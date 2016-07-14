import os
import logging
from logging import handlers
import yaml

import config as config

DEFAULT_LOG_CONFIG = yaml.load(open(config.get_preference(config.LOG_PROPERTIES_PATH)))
DEFAULT_LOG_LEVEL = getattr(logging, DEFAULT_LOG_CONFIG['default.log.level'])
DEFAULT_LOG_FORMAT = logging.Formatter(DEFAULT_LOG_CONFIG['default.log.format'])
DEFAULT_LOG_DIR = os.path.abspath(DEFAULT_LOG_CONFIG['default.log.dir'])

logging.basicConfig(
    level=DEFAULT_LOG_LEVEL,
    format=DEFAULT_LOG_CONFIG['default.log.format']
)
logging.getLogger()
# print logging._handlerList
# map(logging._removeHandlerRef, logging._handlerList)


CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


def _get_default_handler(**kwargs):
    default_handler = DEFAULT_LOG_CONFIG['default.log.handler']

    if default_handler == 'RotatingFileHandler':
        adapted_kwargs = dict(
            (key, kwargs[key]) for key in get_rotating_file_handler.func_code.co_varnames if key in kwargs)
        return get_rotating_file_handler(**adapted_kwargs)
    elif default_handler == 'SocketHandler':
        adapted_kwargs = dict(
            (key, kwargs[key]) for key in get_socket_handler.func_code.co_varnames if key in kwargs)
        return get_socket_handler(**adapted_kwargs)
    elif default_handler == 'DatagramHandler':
        adapted_kwargs = dict(
            (key, kwargs[key]) for key in get_datagram_handler.func_code.co_varnames if key in kwargs)
        return get_datagram_handler(**adapted_kwargs)
    elif default_handler == 'HTTPHandler':
        adapted_kwargs = dict(
            (key, kwargs[key]) for key in get_http_handler.func_code.co_varnames if key in kwargs)
        return get_http_handler(**adapted_kwargs)
    elif default_handler == 'SMTPHandler':
        adapted_kwargs = dict(
            (key, kwargs[key]) for key in get_smtp_handler.func_code.co_varnames if key in kwargs)
        return get_smtp_handler(**adapted_kwargs)
    else:
        # TODO: raise unsupported handler exception
        pass


def get_rotating_file_handler(path, level=DEFAULT_LOG_LEVEL, formatter=DEFAULT_LOG_FORMAT,
                              mode=None, maxBytes=None, backupCount=0, encoding=None, delay=None):
    options = DEFAULT_LOG_CONFIG['RotatingFileHandler']

    mode = mode if mode else options['mode']
    maxBytes = maxBytes if maxBytes else options['maxBytes']
    backupCount = backupCount if backupCount else options['backupCount']
    encoding = encoding if encoding else options['encoding']
    delay = delay if delay else options['delay']

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    handler = handlers.RotatingFileHandler(path, mode, maxBytes, backupCount, encoding, delay)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


def get_socket_handler(level=DEFAULT_LOG_LEVEL, formatter=DEFAULT_LOG_FORMAT, host=None, port=None):
    options = DEFAULT_LOG_CONFIG['SocketHandler']
    host = host if host else options['host']
    port = port if port else options['port']

    handler = handlers.SocketHandler(host, port)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


def get_datagram_handler(level=DEFAULT_LOG_LEVEL, formatter=DEFAULT_LOG_FORMAT, host=None, port=None):
    options = DEFAULT_LOG_CONFIG['DatagramHandler']
    host = host if host else options['host']
    port = port if port else options['port']

    handler = handlers.DatagramHandler(host, port)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


def get_http_handler(level=DEFAULT_LOG_LEVEL, formatter=DEFAULT_LOG_FORMAT, host=None, url=None, method=None):
    options = DEFAULT_LOG_CONFIG['HTTPHandler']
    host = host if host else options['host']
    url = url if url else options['url']
    method = method if method else options['method']

    handler = handlers.HTTPHandler(host, url, method=method)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


def get_smtp_handler(level=DEFAULT_LOG_LEVEL,
                     formatter=DEFAULT_LOG_FORMAT,
                     host=None,
                     fromaddr=None,
                     toaddrs=None,
                     subject=None):
    options = DEFAULT_LOG_CONFIG['SMTPHandler']
    host = host if host else options['host']
    host = host.split(':')

    fromaddr = fromaddr if fromaddr else options['fromaddr']
    toaddrs = toaddrs if toaddrs else options['toaddrs']
    subject = subject if subject else options['subject']

    handler = handlers.SMTPHandler((host[0], host[1]),
                                   fromaddr,
                                   toaddrs,
                                   subject)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


root_logger = None
loggers = {}


def _init_root_logger():
    global root_logger
    root_logger = logging.getLogger(DEFAULT_LOG_CONFIG['default.log.root'])
    root_handler_config = DEFAULT_LOG_CONFIG['root']
    root_handler_name = DEFAULT_LOG_CONFIG['default.log.handler']
    root_handler_options = DEFAULT_LOG_CONFIG[root_handler_name]
    root_handler_options.update(root_handler_config['root.handler.options'])

    root_handler = _get_default_handler(**root_handler_options)
    root_logger.addHandler(root_handler)


# initialize root logger
_init_root_logger()


def getRootLogger():
    return root_logger


def getLogger(name, handler=None, propagate=False):
    if name not in loggers:
        logger = logging.getLogger(name)
        logger.propagate = propagate
        logger.addHandler(handler if handler else _get_default_handler())
        loggers[name] = logger

    return loggers[name]
