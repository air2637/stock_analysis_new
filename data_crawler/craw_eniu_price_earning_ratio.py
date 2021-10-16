import asyncio
import os
import re
from datetime import datetime

import aiohttp
import pandas as pd

from setup_logging import logger


async def read_url(url) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            return content


async def write_data(filename, content) -> None:
    with open(filename, "wb+") as f:
        f.write(content)
    logger.info("Finishing writing %s", filename)


async def convert_csv(filename, stock_id, stock_name) -> None:
    df = pd.read_json(filename)
    df["stock_id"] = stock_id
    df["stock_name"] = stock_name
    df.to_csv(filename)


async def single_task_wrapper(url, filename, stock_id, stock_name):
    try:
        content = await read_url(url)
        await write_data(filename, content)
        await convert_csv(filename, stock_id, stock_name)
    except Exception as e:
        logger.error("Exception handling %s from %s - Exception details: %s", stock_id, url, e)


async def iterate_stocks(df_all_stock, store_dir, store_url):
    tasks = []
    for index, row in df_all_stock.iterrows():
        url = re.sub(r'\{stock_id}', row.stock_id, store_url)
        filename = os.path.join(store_dir, row.stock_id + ".csv")
        tasks.append(single_task_wrapper(url, filename, row.stock_id, row.stock_name))
    await asyncio.wait(tasks)


async def iterate_stocks_wrapper(df_all_stock, store_dir, store_url, step_val):
    lower = 0
    max_rows = df_all_stock.shape[0]
    for upper in range(step_val, max_rows, step_val):
        logger.info("Downloading group between %s to %s", lower, upper)
        await iterate_stocks(df_all_stock[lower:upper], store_dir, store_url)
        lower = upper
    logger.info("Downloading group between %s to %s", lower, max_rows)
    await iterate_stocks(df_all_stock[lower:max_rows], store_dir, store_url)


def craw(store_url, store_dir, stock_id_dir):
    """ Get the historical price to earning ratio for all stocks in stock_id_dir """
    logger.info("craw_eniu_price_earning_ratio from %s, and to download to %s", store_url, store_dir)
    cwd = os.getcwd()
    store_dir = os.path.join(cwd, store_dir)
    stock_id_dir = os.path.join(cwd, stock_id_dir, "stock_id.csv")
    df_all_stock = pd.read_csv(stock_id_dir, dtype=str)
    time_start = datetime.now()
    asyncio.run(iterate_stocks_wrapper(df_all_stock, store_dir, store_url, 20))
    logger.info("Total spent %s seconds", (datetime.now() - time_start).total_seconds())
