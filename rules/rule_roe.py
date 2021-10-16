
from setup_logging import logger


def apply_rule(raw_data_loc, min_roe, roe_type):
    logger.info("%s is called "
                "with raw_data_loc = %s, min_roe = %s, roe_type = %s",
                __name__, raw_data_loc, min_roe, roe_type)