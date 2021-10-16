import re

from setup_logging import logger
import os
import pandas as pd

def craw(store_url, store_dir, stock_id_dir):
    """extract net profit data from url provided,
        and download the data to dir specified
    """
    logger.info("craw_eniu_net_profit from %s, and to download to %s", store_url, store_dir)
    cwd = os.getcwd()
    store_dir = os.path.join(cwd, store_dir)
    stock_id_dir = os.path.join(cwd, stock_id_dir, "stock_id.csv")

    # Load stock ids from /data/stock_id/stock_id.csv
    df_all_stocks = pd.read_csv(stock_id_dir, dtype=str)
    for index, row in df_all_stocks.iterrows():
        net_profit_url = re.sub(r"\{stock_id\}", row.stock_number, store_url)
        logger.info("Stock net profit url: %s", net_profit_url)
        


    
