import logging
import os

class Logger():
    def __init__(self, log_path):
        # Verificar si la carpeta logs existe, si no, crearla
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        
        self.log_path = log_path
        logging.basicConfig(
            filename=self.log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
        )
    
    def logInfo(self, message):
        logging.info(message)
        
    def logError(self, message):
        logging.error(message)
        
    def logWarning(self, message):
        logging.warning(message)
        
    def logDebug(self, message):
        logging.debug(message) 
    
    def close(self):
        logging.info('Closing sample program')
        logging.shutdown()