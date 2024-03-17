import logging

class CustomLogger:
    def __init__(self, debug_mode=False, log_file=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        # File Handler
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG if debug_mode else logging.INFO)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        
    def debug(self, message):
        self.logger.debug(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def critical(self, message):
        self.logger.critical(message)
