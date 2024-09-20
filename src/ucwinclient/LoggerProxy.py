import logging

class LoggerProxy:
    def __init__(self, LoggerName, FileName):
        self.LoggerName = LoggerName
        logger = logging.getLogger(LoggerName)
        logger.setLevel(20)
        self.sh = logging.StreamHandler()
        logger.addHandler(self.sh)
        self.fh = logging.FileHandler(FileName)
        logger.addHandler(self.fh)
        formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(thread)d:%(levelname)s:%(funcName)s:%(message)s')
        self.fh.setFormatter(formatter)
        self.sh.setFormatter(formatter)

    @property
    def logger(self):
        return logging.Logger.manager.loggerDict[self.LoggerName]

    def killLogger(self):
        self.fh.close()
        self.sh.close()
        del logging.Logger.manager.loggerDict[self.LoggerName]


