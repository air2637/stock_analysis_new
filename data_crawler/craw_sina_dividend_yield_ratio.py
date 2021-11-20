import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from setup_logging import logger


def craw(store_url, store_dir, max_page_enforced=None, start_page=None):
    """
    The crawler load sina's url with page parameter and save it into a csv file

    :param store_url: sina's url for Dividend Yield Ratio historical data
    :param store_dir: path for storing the crawled results
    :param url_page: not need I think
    :return: None
    """
    logger.info("craw_eniu_stock_id from %s, and to download to %s", store_url, store_dir)
    cwd = os.getcwd()
    file_path = os.path.join(cwd, store_dir, "stock_dividend_yield_ratio.csv")

    page = 1 if start_page is None else start_page
    num_record_per_page = "60"
    max_page = page
    dfs = []

    while page <= max_page:
        single_df, max_page = load_data_from_page(store_url, page, num_record_per_page)
        max_page = max_page if max_page_enforced is None else max_page_enforced
        page += 1
        dfs.append(single_df)

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(file_path)


def load_data_from_page(url, page, num):
    res = requests.get(url, params={'p': page, 'num': num}, headers={'user-agent': 'Mozilla/5.0 ', 'Accept-Encoding': 'gzip'})
    logger.info("loading from %s", res.url)
    soup = BeautifulSoup(res.text, "html.parser")
    '''load dataframe'''
    data_table = soup.find(id="dataTable")
    trs = data_table.findChildren("tr")
    columns = []
    single_row = []
    rows = []
    for i in range(len(list(trs))):
        cells = trs[i].findChildren("td")
        for j in range(len(list(cells))):
            if i == 0:
                columns.append(cells[j].string)
            else:
                single_row.append(cells[j].string)
        if len(single_row):
            rows.append(single_row)
            single_row = []
    df = pd.DataFrame(rows, columns=columns)
    '''load max page'''
    pages = soup.find_all("a", {"class":"page"})
    max_page = int(pages[len(pages)-2].string)

    return df, max_page

