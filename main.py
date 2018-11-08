import os
import begin
import logging
from logging.handlers import RotatingFileHandler
import json

LOGGER = 0


def create_loggers(logs_file: str, errors_file: str):
    """ Create the logger for all information"""

    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

    file_handler = RotatingFileHandler(logs_file, 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    file_handler = RotatingFileHandler(errors_file, 'a', 1000000, 1)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)

    return logger


def data_checking(data, i):
    """checking through the request data for errors or missing arguments
    before calling request function"""
    global LOGGER
    #protocol :
    if("protocol" in data):
        if(data["protocol"] == None or data["protocol"] == ""):
            LOGGER.error("No value given for argument protocol in request %s" %i)
            return
        if(type(data["protocol"]) is not str):
            LOGGER.error("Wrong data type for protocol in request %s" %i)
            return
        if(type(data["protocol"]) is list):
            LOGGER.error("Too many arguments for protocol in request %s" %i)
            return
    else:
        LOGGER.error("No protocol found in request %s" %i)
        return
    #access_token
    if("access_token" in data):
        if(data["access_token"] == None or data["access_token"] == ""):
            LOGGER.error("No value given for argument access_token in request %s" %i)
            return
        if(type(data["access_token"]) is not str):
            LOGGER.error("Wrong data type for access_token in request %s" %i)
            return
        if(type(data["access_token"]) is list):
            LOGGER.error("Too many arguments for access_token in request %s" %i)
            return
    else:
        LOGGER.error("No access_token found in request %s" %i)
        return
    #users
    if("users" in data):
        if(data["users"] == None or data["users"] == ""):
            LOGGER.error("No value given for argument users in request %s" %i)
            return
        if(not all(isinstance(x, str) for x in data["users"])):
            LOGGER.error("Wrong data type for users in request %s" %i)
            return
    else:
        LOGGER.error("No users found in request %s" %i)
        return
    #pswds
    if("pswds" in data):
        if(data["pswds"] == None or data["pswds"] == ""):
            LOGGER.error("No value given for argument pswds in request %s" %i)
            return
        if(not all(isinstance(x, str) for x in data["pswds"])):
            LOGGER.error("Wrong data type for pswds in request %s" %i)
            return
    else:
        LOGGER.error("No pswds found in request %s" %i)
        return
    #pswd and users same size
    if(len(data["users"]) != len(data["pswds"])):
        if(len(data["users"]) > len(data["pswds"])):
            LOGGER.error("Missing "+str(len(data["users"]) - len(data["pswds"]))+" passwords in request %s" %i)
        else:
            LOGGER.error("Missing "+str(len(data["pswds"]) - len(data["users"]))+" users in request %s" %i)
    return


@begin.start
@begin.convert(debug=bool)
def run(access_file, logs_file, errors_file, debug=False ):
    """main function : checking arguments and creating logger"""
    global LOGGER
    LOGGER = create_loggers(logs_file, errors_file)

    if os.path.isfile(access_file):
        if os.path.isfile(logs_file):
            if os.path.isfile(errors_file):
                with open(access_file) as json_data:
                    data = json.load(json_data)
                    i = 1
                    for d in data:
                        LOGGER.info("Processing request "+str(i))
                        data_checking(d,i)
                        i += 1
            else:
                logging.error("Error file path is not correct")
                return
        else:
            logging.error("Logs file path is not correct")
            return
    else:
        logging.error("Access file path is not correct")
        return

