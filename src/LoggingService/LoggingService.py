import json
import os
import logging
from pythonjsonlogger import jsonlogger


class LoggingService:
    def __init__(self):
        self = self
        
    def logData(self, data, filePath):
        
        with open(filePath, 'w') as file:
            
            json.dump(data, file, indent=4)
            
        file.close()
