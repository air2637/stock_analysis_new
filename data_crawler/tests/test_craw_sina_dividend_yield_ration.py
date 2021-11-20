from data_crawler import craw_sina_dividend_yield_ratio


def test_craw_single_page():
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml"
    page = "2"
    store_dir = "data/tmp/"
    breakpoint()
    craw_sina_dividend_yield_ratio.craw(url, store_dir, page)