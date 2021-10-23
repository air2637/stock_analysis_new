from rules import *
from setup_logging import logger


def call_rule(rule, kwargs):
    if rule == "rule_net_profit_keeps_increasing":
        rule_net_profit_keeps_increasing.apply_rule(**kwargs)

    elif rule == "rule_price_earning_ratio":
        rule_price_earning_ratio.apply_rule(**kwargs)

    elif rule == "rule_roe":
        rule_roe.apply_rule(**kwargs)

    else:
        logger.warn("rule %s is not registered", rule)


def combine_rule_results(logic_gates):
    pass
