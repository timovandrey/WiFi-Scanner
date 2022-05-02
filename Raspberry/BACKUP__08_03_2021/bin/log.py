from datetime import datetime

LOG_EN = True
LOG_TO_FILE = True

class LogBotException(Exception):
    pass

# Use as following:
# - To only log to console with timestamp, use the static method "LogBot.LOG(<message>)"
# - To log also to a file, instantiate the LogBot with the desired output file as parameter.raise
#   then use the self.LOG() method, to also write to the file.
#   To be able to write to the LOG
class LogBot():
    def __init__(self, logfilepath):
        self.dumpfile = logfilepath
        self.start()

    def start(self):
        try:
            self.log = open(dumpfile, 'w')
        except OSError:
            raise LogBotException("Error occured during dumpfile opening (\"" + dumpfile + "\")")

    def stop(self):
        try:
            self.log.close()
        except OSError:
            raise LogBotException("Error occured during dumpfile closing (\"" + dumpfile + "\")")

    @staticmethod
    def LOG(message):  
        if LOG_EN:
            print(datetime.now().strftime("%H:%M:%S") + ": -> " + message)

    def LOG(self, message):
        if LOG_EN:
            print(datetime.now().strftime("%H:%M:%S") + ": -> " + message)
            if LOG_TO_FILE:
                try:
                    self.log.write(datetime.now().strftime("%H:%M:%S") + ": -> " + message)
                except OSError:
                    try:
                        self.log.write(datetime.now().strftime("%H:%M:%S") + ": -> " + message)
                    except OSError:    
                        raise LogBotException("Error occured during dumpfile closing (\"" + dumpfile + "\")")