import os.path

import pytest
from rules import rule_net_profit_keeps_increasing


@pytest.mark.parametrize("raw_data_loc, result_loc, keeps_increasing_count, net_profit_type", [
    ("", "data/result/", "2", "year"),
])
def test_apply_rule(raw_data_loc, result_loc, keeps_increasing_count, net_profit_type):
    raw_data_loc = os.path.join(os.getcwd(), "rules/tests/test_tmp_folder1")
    stock_wanted = rule_net_profit_keeps_increasing\
        .apply_rule(raw_data_loc, result_loc, keeps_increasing_count, net_profit_type)
    expected = [{
        "stock_id": "sh600008",
        "stock_name": "首创环保",
        "rule_applied": "rules.rule_net_profit_keeps_increasing"
    }]
    assert expected == stock_wanted
