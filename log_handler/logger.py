import logging
import os


class Logger:
    def __init__(self, log_file='application.log', default_level=logging.INFO):
        """
        Initialize the logger with console and file handlers.

        :param log_file: Path to the log file.
        :param default_level: Default logging level.
        """
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(default_level)

        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """
        Get the configured logger instance.

        :return: Configured logger instance.
        """
        return self.logger
