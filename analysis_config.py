config_stock_filter_rules = {

    "logic_gates": "rule_net_profit_keeps_increasing and rule_roe",

    "rules": [
        {"rule_net_profit_keeps_increasing": {
            "raw_data_loc": "data/net_profit/",
            "result_loc": "data/result/",
            "keeps_increasing_count": "5",
            "net_profit_type": "year"
        }, "enabled": True},

        {"rule_price_earning_ratio": {
            "raw_data_loc": "data/price_earning_ratio/",
            "result_loc": "data/result/",
            "percentile_threshold": "0.1",
            "percentile_date_range": "5 years",
            "max_per": "20"
        }, "enabled": True},

        {"rule_roe": {
            "raw_data_loc": "",
            "result_loc": "data/result/",
            "min_roe": "",
            "roe_type": ""
        }, "enabled": False}
    ]
}

config_download_raw_data = {

    "data_stores": [
        {"store_name": "亿牛：股票代码", "store_ulr": "https://eniu.com/static/data/stock_list.json",
         "store_dir": "data/stock_id/", "extract_func": "craw_eniu_stock_id", "refresh_now": False},

        {"store_name": "亿牛：净利润", "store_ulr": "https://eniu.com/chart/profita/{stock_id}/q/0",
         "store_dir": "data/net_profit/", "stock_id_dir": "data/stock_id/",
         "extract_func": "craw_eniu_net_profit", "refresh_now": False},

        {"store_name": "亿牛：市盈率", "store_ulr": "https://eniu.com/chart/pea/{stock_id}/t/all",
         "store_dir": "data/price_earning_ratio", "stock_id_dir": "data/stock_id/",
         "extract_func": "craw_eniu_price_earning_ratio", "refresh_now": False}
    ]
}
