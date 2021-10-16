import os

from setup_logging import logger
import pandas as pd


def apply_rule(raw_data_loc, keeps_increasing_count, net_profit_type):
    logger.info("%s is called "
                "with raw_data_loc = %s, keeps_increasing_count = %s, net_profit_type = %s",
                __name__, raw_data_loc, keeps_increasing_count, net_profit_type)

    '''read net profit for each file in the dir raw_data_loc,
        if it keeps increasing for keeps_increasing_count then kept it in the list
    '''
    cwd = os.getcwd()
    net_profit_dir = os.path.join(cwd, raw_data_loc)
    stock_wanted = []
    for filename in os.listdir(net_profit_dir):
        with open(os.path.join(net_profit_dir, filename), 'r') as f:
            df = pd.read_csv(f)
            if check_keeps_increasing_count(df, int(keeps_increasing_count)):
                stock_wanted.append({"stock_id": df.loc[0, "stock_id"], "stock_name": df.loc[0, "stock_name"]})
    logger.info("stock_wanted: %s", stock_wanted)
    return stock_wanted


def check_keeps_increasing_count(df, keeps_increasing_count):
    start_index = 0 if df.shape[0] < keeps_increasing_count else (df.shape[0] - keeps_increasing_count)
    max_index = (df.shape[0] - 1) if df.shape[0] > 1 else 0
    previous_val = df.loc[max_index, "profit"]
    for i in range(max_index - 1, start_index - 1, -1):
        # logger.info("current i: %s, profit: %s, previous_val: %s, stock: %s, start_index: %s",
        #             i, df.loc[i, "profit"], previous_val, df.loc[i, "stock_id"], start_index)
        if df.loc[i, "profit"] > previous_val:
            return False
        previous_val = df.loc[i, "profit"]
    return True
