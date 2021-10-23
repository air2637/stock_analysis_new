import datetime
import os
import re
from datetime import date, timedelta

from setup_logging import logger
import pandas as pd


def apply_rule(raw_data_loc, percentile_threshold, percentile_date_range, max_per):
    """1. Read per data from raw_data_loc

       2. if percentile_threshold and percentile_date_range specified,
       to filter out stocks current per exceeds the percentile_threshold
       in given date range percentile_date_range

       3. if max_per specified,
       to filter out stocks current per exceeds the max_per
    """

    logger.info("%s is called "
                "with raw_data_loc = %s, percentile_threshold = %s, percentile_date_range = %s, max_per = %s",
                __name__, raw_data_loc, percentile_threshold, percentile_date_range, max_per)

    cwd = os.getcwd()
    per_dir = os.path.join(cwd, raw_data_loc)
    stock_wanted = []
    for file in os.listdir(per_dir):
        try:
            df = pd.read_csv(os.path.join(per_dir, file))
            df['date'] = pd.to_datetime(df['date']).dt.date
            result_filter_by_max_per = filter_by_max_per(df, max_per)
            result_filter_by_percentile = filter_by_percentile(df, percentile_threshold, percentile_date_range)
            logger.debug("result_filter_by_max_per: %s, result_filter_by_percentile: %s", result_filter_by_max_per,
                         result_filter_by_percentile)
            if result_filter_by_max_per and result_filter_by_percentile:
                stock_wanted.append({"stock_id": df.loc[0, "stock_id"], "stock_name": df.loc[0, "stock_name"]})
        except Exception as e:
            logger.error("Error in loading %s - Error details: %s", file, e)
    logger.info("stock_wanted: %s", stock_wanted)
    return stock_wanted


def filter_by_percentile(df, percentile_threshold, percentile_date_range) -> bool:
    target_date = extract_date(percentile_date_range)
    pe_ttm_series = df[df['date'] >= target_date].pe_ttm
    pe_ttm_latest = df.iloc[-1]["pe_ttm"]
    pe_ttm_quantile = pe_ttm_series.quantile(float(percentile_threshold))
    logger.debug("pe_ttm_latest %s, pe_ttm_%s %s within %s", pe_ttm_latest, percentile_threshold, pe_ttm_quantile, percentile_date_range)
    return pe_ttm_quantile >= pe_ttm_latest


def filter_by_max_per(df, max_per) -> bool:
    # logger.debug("filter_by_max_per with %s", df.loc[0, "stock_id"])
    if max_per == "":
        return True
    if df.iloc[-1]["pe_ttm"] > float(max_per) or df.iloc[-1]["pe_ttm"] <= 0:
        return False
    return True


def extract_date(date_range, from_date=date.today()) -> date:
    matched = re.search("(\d+)\s?([ymd])", date_range, re.IGNORECASE)
    if matched is None:
        raise ValueError(f"No matched date_range found for input: {date_range}")
    n = int(matched.group(1))
    unit = matched.group(2)

    if unit.upper() == "Y":
        return from_date - datetime.timedelta(days=n * 365)
    elif unit.upper() == "M":
        return from_date - datetime.timedelta(days=n * 30)
    elif unit.upper() == "D":
        return from_date - datetime.timedelta(days=n)
    else:
        return None
