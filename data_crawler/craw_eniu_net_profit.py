import re

import requests

from setup_logging import logger
import os
import pandas as pd
import asyncio
import aiohttp
from aiohttp import ClientSession


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

    # asyncio.run(get_url_and_download(df_all_stocks, store_url, store_dir, cwd))

    for index, row in df_all_stocks.iterrows():
        net_profit_url = re.sub(r"\{stock_id\}", row.stock_id, store_url)
        file_path = os.path.join(cwd, store_dir, row.stock_id + ".csv")
        logger.info("Stock net profit url: %s", net_profit_url)
        go_download(net_profit_url, file_path, row.stock_id, row.stock_name)


async def get_url_and_download(df_all_stocks, store_url, store_dir, cwd):
    async with ClientSession() as session:
        for index, row in df_all_stocks.iterrows():
            net_profit_url = re.sub(r"\{stock_id\}", row.stock_id, store_url)
            file_path = os.path.join(cwd, store_dir, row.stock_id + ".csv")
            logger.info("Stock net profit url: %s", net_profit_url)
            asyncio.create_task(go_download(session, net_profit_url, file_path, row.stock_id, row.stock_name))


def go_download(net_profit_url, file_path, stock_id, stock_name):
    df_stock_net_profit = pd.read_json(net_profit_url)
    df_stock_net_profit["stock_id"] = stock_id
    df_stock_net_profit["stock_name"] = stock_name
    df_stock_net_profit.to_csv(file_path)
