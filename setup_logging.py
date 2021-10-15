import logging

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s %(message)s', filemode='w')
logger.setLevel(logging.INFO)