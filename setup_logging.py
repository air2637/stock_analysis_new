import logging

logger = logging.getLogger()
logging.basicConfig(filename="APP_DEBUG.log", format='%(asctime)s[%(levelname)s]-%(message)s', filemode='w')
logger.setLevel(logging.DEBUG)