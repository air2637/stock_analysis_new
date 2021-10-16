from data_crawler import *
from setup_logging import logger


def crawl_by(func, param_dict):
    # breakpoint()

    if func == "craw_eniu_stock_id":
        craw_eniu_stock_id.craw(param_dict["store_ulr"], param_dict["store_dir"])

    elif func == "craw_eniu_net_profit":
        craw_eniu_net_profit.craw(param_dict["store_ulr"], param_dict["store_dir"], param_dict["stock_id_dir"])

    else:
        logger.warn("%s func name not found", func)
