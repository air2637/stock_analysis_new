import pandas as pd

from rules import *
from setup_logging import logger


def call_rule(rule, kwargs):
    if rule == "rule_net_profit_keeps_increasing":
        return rule_net_profit_keeps_increasing.apply_rule(**kwargs)

    if rule == "rule_price_earning_ratio":
        return rule_price_earning_ratio.apply_rule(**kwargs)

    if rule == "rule_roe":
        return rule_roe.apply_rule(**kwargs)

    else:
        logger.warn("rule %s is not registered", rule)
        return None


def combine_rule_results(result_files, logic_gates):
    final_df = pd.DataFrame()
    for result_file in result_files:
        df = pd.read_csv(result_file).iloc[:, 1:]
        df.set_index("stock_id", inplace=True)
        final_df = pd.concat([final_df, df], axis=1)

    utils.save_result(final_df, "data/result/", "final_result")
