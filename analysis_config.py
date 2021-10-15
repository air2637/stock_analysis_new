config_stock_filter_rules = {

    "logic_gates": "rule_net_profit_keeps_increasing and rule_roe",

    "rules": [
        {"rule_net_profit_keeps_increasing": {
            "raw_data_loc": "some loc here",
            "keeps_increasing_count": "1",
            "net_profit_type": "year"
        }},
        {"rule_roe": {
            "raw_data_loc": "",
            "min_roe": "",
            "roe_type": ""
        }}
    ]
}
