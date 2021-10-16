config_stock_filter_rules = {

    "logic_gates": "rule_net_profit_keeps_increasing and rule_roe",

    "rules": [
        {"rule_net_profit_keeps_increasing": {
            "raw_data_loc": "data/net_profit/",
            "keeps_increasing_count": "3",
            "net_profit_type": "year"
        }},
        {"rule_roe": {
            "raw_data_loc": "",
            "min_roe": "",
            "roe_type": ""
        }}
    ]
}

config_download_raw_data = {

    "data_stores": [
        {"store_name": "亿牛：股票代码", "store_ulr": "https://eniu.com/static/data/stock_list.json",
         "store_dir": "data/stock_id/", "extract_func": "craw_eniu_stock_id", "refresh_now": False},
        {"store_name": "亿牛：净利润", "store_ulr": "https://eniu.com/chart/profita/{stock_id}/q/0",
         "store_dir": "data/net_profit/", "stock_id_dir": "data/stock_id/",
         "extract_func": "craw_eniu_net_profit", "refresh_now": True},
        {"store_name": "", "store_ulr": "", "store_dir": "", "extract_func": "", "refresh_now": False}
    ]
}
