import logging.config
import logging.handlers
import json
import atexit
import inspect
import platform

if platform.system() == "Windows":
    LOGGER_CONFIG_PATH = r"config\logging_config.json"
elif platform.system() == "Linux":
    LOGGER_CONFIG_PATH = "config/logging_config.json"
else:
    print("Unrecognized OS!")


class Logger():

    def __init__(self):
        """"""
        self.logger = logging.getLogger("__name__")

        config_file = LOGGER_CONFIG_PATH

        self._setup_logging(config_file=config_file)

    def _setup_logging(self, config_file):
        """"""
        # Load in our logging config
        with open(config_file) as f:
            config = json.load(f)

        # Apply our logging configs
        logging.config.dictConfig(config)

        # setup our queue handler:
        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)

    def _retrieve_caller_func(self) -> str:
        # Retrieve caller information using inspect module
        frame = inspect.currentframe().f_back.f_back.f_back # use f_back three times to get original function
        func_name = frame.f_code.co_name
        line_number = frame.f_lineno
        return func_name, line_number


    def log(self, level, msg):
        """"""
        # retrieve calling function and lin number
        func_name, line_number = self._retrieve_caller_func()
        # Format log message with caller information
        formatted_msg = f"{func_name} (line {line_number}): {msg}"
        getattr(self.logger, level)(formatted_msg)


    def info(self, msg):
        self.log('info', msg)

    def warning(self, msg):
        self.log('warning', msg)

    def error(self, msg):
        self.log('error', msg)

    def critical(self, msg):
        self.log('critical', msg)



