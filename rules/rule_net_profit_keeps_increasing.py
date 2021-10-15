from setup_logging import logger


def apply_rule(raw_data_loc, keeps_increasing_count, net_profit_type):
    logger.info("%s is called "
                "with raw_data_loc = %s, keeps_increasing_count = %s, net_profit_type = %s",
                __name__, raw_data_loc, keeps_increasing_count, net_profit_type)


