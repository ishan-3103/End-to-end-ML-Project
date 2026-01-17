import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):   ## error_detail is just a variable to represent sys module
    _,_,exc_tb=error_detail.exc_info()      ## exc_info() returns 3 values.  _,_, means we dont care about first 2 values. 3rd value is error traceback
    file_name=exc_tb.tb_frame.f_code.co_filename    ## just extracts in which file the error has occured
    error_message=f"Error occuered in python script name {file_name} line number {exc_tb.tb_lineno} error message{str(error)}"

    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail)

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    import sys
    try:
        a=1/ 0
    except Exception as e:
        logging.info("logging has started")
        raise CustomException(e, sys)

