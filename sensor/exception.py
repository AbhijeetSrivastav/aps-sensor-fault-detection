import os
import sys


def error_message_detail(error, error_detail: sys):
    """
    Extract error causing script, error causing line, error 
    --------------------------------------------------------
    error: error message from SensorException class
    error_detail: error details from SensorException class
    ---------------------------------------------------------
    return: error_message
    """

    # exc_tb : exception traceback
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    error_message = "Python script: [{0}]   Line number: [{1}]  Error  message: [{2}]".format(file_name, exc_tb.tb_lineno, str(error))

    return error_message



class SensorException(Exception):
    """
    Raise SensorException 
    ------------------------------------------------
    return: sensor exception error message
    """
    def __init__(self, error_message, error_detail: sys):
        self.error_message = error_message_detail(error=error_message, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message