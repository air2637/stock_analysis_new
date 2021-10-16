from datetime import datetime
import re
from setup_logging import logger
import os
import pandas as pd
import asyncio
import aiohttp


async def read_url(url) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            return content


async def write_data(filename, content) -> None:
    with open(filename, "wb+") as f:
        f.write(content)
    logger.info("Finishing writing %s", filename)


async def convert_csv(filename, stock_id, stock_name):
    df_stock_net_profit = pd.read_json(filename)
    df_stock_net_profit["stock_id"] = stock_id
    df_stock_net_profit["stock_name"] = stock_name
    df_stock_net_profit.to_csv(filename)


async def single_task_wrapper(url, filename, stock_id, stock_name) -> None:
    try:
        content = await read_url(url)
        await write_data(filename, content)
        await convert_csv(filename, stock_id, stock_name)
    except Exception as e:
        logger.error("Exception handling %s from %s - Exception details: %s", stock_id, url, e)


async def iterate_stocks(df_all_stocks, store_dir, store_url) -> None:
    tasks = []
    for index, row in df_all_stocks.iterrows():
        net_profit_url = re.sub(r"\{stock_id}", row.stock_id, store_url)
        filename = os.path.join(store_dir, row.stock_id + ".csv")
        tasks.append(single_task_wrapper(net_profit_url, filename, row.stock_id, row.stock_name))
    await asyncio.wait(tasks)


async def iterate_stocks_wrapper(df_all_stocks, store_dir, store_url, step_val) -> None:
    lower = 0
    max_rows = df_all_stocks.shape[0]
    for upper in range(step_val, max_rows, step_val):
        logger.info("Downloading group between %s to %s", lower, upper)
        await iterate_stocks(df_all_stocks[lower:upper], store_dir, store_url)
        lower = upper
    logger.info("Downloading group between %s to %s", lower, max_rows)
    await iterate_stocks(df_all_stocks[lower:max_rows], store_dir, store_url)


def craw(store_url, store_dir, stock_id_dir):
    """extract net profit data from url provided,
        and download the data to dir specified
    """
    logger.info("craw_eniu_net_profit from %s, and to download to %s", store_url, store_dir)

    cwd = os.getcwd()
    store_dir = os.path.join(cwd, store_dir)
    stock_id_dir = os.path.join(cwd, stock_id_dir, "stock_id.csv")
    df_all_stocks = pd.read_csv(stock_id_dir, dtype=str)
    time_start = datetime.now()
    asyncio.run(iterate_stocks_wrapper(df_all_stocks, store_dir, store_url, 20))
    logger.info("Total spent %s seconds", (datetime.now() - time_start).total_seconds())
