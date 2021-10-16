from setup_logging import logger
import os
import pandas as pd


def craw(store_url, store_dir):
    """extract net profit data from url provided,
        and download the data to dir specified
    """
    logger.info("craw_eniu_stock_id from %s, and to download to %s", store_url, store_dir)
    cwd = os.getcwd()
    file_path = os.path.join(cwd, store_dir, "stock_id.csv")
    df = pd.read_json(store_url, dtype=str)
    df = df[(~df.stock_name.str.contains('ST|st', regex=True)) & (df.stock_number.str.len() == 6)]
    df.to_csv(file_path)
