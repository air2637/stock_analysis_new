import os

from data_crawler import *
from setup_logging import logger


def crawl_by(func, param_dict):

    if param_dict["refresh_now"]:
        cwd = os.getcwd()
        path = os.path.join(cwd, param_dict["store_dir"])
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

    if func == "craw_eniu_stock_id":
        craw_eniu_stock_id.craw(param_dict["store_ulr"], param_dict["store_dir"])

    elif func == "craw_eniu_net_profit":
        craw_eniu_net_profit.craw(param_dict["store_ulr"], param_dict["store_dir"], param_dict["stock_id_dir"])

    elif func == "craw_eniu_price_earning_ratio":
        craw_eniu_price_earning_ratio.craw(param_dict["store_ulr"], param_dict["store_dir"], param_dict["stock_id_dir"])

    elif func == "craw_sina_dividend_yield_ratio":
        craw_sina_dividend_yield_ratio.craw(param_dict["store_ulr"], param_dict["store_dir"],
                                            param_dict["max_page_enforced"], param_dict["start_page"])

    else:
        logger.warn("%s func name not found", func)
