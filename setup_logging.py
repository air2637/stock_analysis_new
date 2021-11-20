import logging

logger = logging.getLogger()
logging.basicConfig(filename="APP_DEBUG.log", format='%(asctime)s[%(levelname)s]-%(message)s', filemode='w')
# logging.basicConfig(format='%(asctime)s[%(levelname)s]-%(message)s')
logger.setLevel(logging.DEBUG)