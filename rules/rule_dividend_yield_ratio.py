import os
from datetime import date, timedelta

import pandas as pd

from rules import utils
from setup_logging import logger


def apply_rule(raw_data_loc, result_loc, percentage_threshold, frequency_dividend_since_listed,
               cumulative_dividend_threshold):
    """1. Read dividend yield ratio data from raw_data_loc

       2. if percentage_threshold is specified, find stock with dividend yield ratio above percentage_threshold

       3. if frequency_dividend_since_listed is specified, find stock which frequency of dividend above the threshold
       frequency_dividend_since_listed

       4. if cumulative_dividend_threshold is specified, find stock which cumulative dividend ratio above the threshold

       5. find the overlap of above filter results
    """

    logger.info("""%s is called 
                     with raw_data_loc = %s, result_loc = %s, percentage_threshold = %s, 
                     frequency_dividend_since_listed = %s, cumulative_dividend_threshold = %s
                """,
                __name__, raw_data_loc, result_loc, percentage_threshold, frequency_dividend_since_listed,
                cumulative_dividend_threshold)

    dividend_yield_ratio_file = os.path.join(os.getcwd(), raw_data_loc)
    stock_wanted = []
    try:
        with open(dividend_yield_ratio_file, 'r') as f:
            df = pd.read_csv(f, dtype={'代码': str})
            df.drop(df.columns[0], axis=1, inplace=True)
            df.rename(columns={"代码": "stock_id",
                               "名称": "stock_name",
                               "上市日期": "listed_on",
                               "累计股息(%)": "cumulative",
                               "年均股息(%)": "average",
                               "分红次数": "dividend_counts"
                            }, inplace=True)

            r1 = dividend_yield_ration_above(df, percentage_threshold)
            r2 = frequency_dividend_since_listed_above(df, frequency_dividend_since_listed)
            r3 = cumulative_dividend_yield_ratio_above(df, cumulative_dividend_threshold)
            r_1_2 = pd.merge(r1, r2, how='inner', on=['stock_id', 'stock_name']).drop_duplicates()
            stock_wanted = pd.merge(r_1_2, r3, how='inner', on=['stock_id', 'stock_name']).drop_duplicates()

    except Exception as e:
        logger.error("Error in loading %s - Error details: %s", dividend_yield_ratio_file, e)

    stock_wanted[__name__.replace("rules.", "")] = True
    return utils.save_result(pd.DataFrame(stock_wanted), result_loc, __name__)


def dividend_yield_ration_above(df, percentage_threshold):
    if percentage_threshold is None:
        return df[['stock_id', 'stock_name']]
    wanted = df[df['average'] >= float(percentage_threshold)]
    return wanted[['stock_id', 'stock_name']]


def frequency_dividend_since_listed_above(df, frequency_dividend_since_listed):
    if frequency_dividend_since_listed is None:
        return df[['stock_id', 'stock_name']]
    df['listed_on'] = pd.to_datetime(df['listed_on'])
    df['today'] = pd.to_datetime(date.today())
    df['years_count'] = (df['today'] - df['listed_on']) / timedelta(days=365)
    df['freq'] = (df['dividend_counts'].divide(df['years_count']))
    wanted = df[df['freq'] >= float(frequency_dividend_since_listed)]
    return wanted[['stock_id', 'stock_name']]


def cumulative_dividend_yield_ratio_above(df, cumulative_dividend_threshold):
    if cumulative_dividend_threshold is None:
        return df[['stock_id', 'stock_name']]
    wanted = df[df['cumulative'] >= float(cumulative_dividend_threshold)]
    return wanted[['stock_id', 'stock_name']]
