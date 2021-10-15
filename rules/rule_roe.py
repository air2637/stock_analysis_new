
from setup_logging import logger


def apply_rule(raw_data_loc, keeps_increasing_count, net_profit_type):
    logger.info("I am in RuleNetProfitKeepsIncreasing, \
                with raw_data_loc = %s, \
                keeps_increasing_count = %s, net_profit_type = %s",
                raw_data_loc, keeps_increasing_count, net_profit_type)