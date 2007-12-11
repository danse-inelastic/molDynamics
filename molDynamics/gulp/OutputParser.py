from pyparsing import *


class OutputParser:
    
    def __init__(self):
        

        f=file(self.i.logFilename)
        try:
            for line in f:
                pass
        finally:
            f.close()