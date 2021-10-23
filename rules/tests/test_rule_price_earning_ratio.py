import os

import pytest
import pandas as pd
from datetime import datetime, date
from rules import rule_price_earning_ratio


@pytest.mark.parametrize("date_range, from_date_str, outcome", [
    ("1y", "Oct 23 2021", "Oct 23 2020"),
    ("2 years", "Oct 23 2021", "Oct 24 2019"),
    ("1m", "Oct 23 2021", "Sep 23 2021"),
    ("2months", "Oct 24 2021", "Aug 25 2021"),
    ("1d", "Oct 23 2021", "Oct 22 2021"),
    ("2 days", "Oct 23 2021", "Oct 21 2021")
])
def test_extract_date(date_range, from_date_str, outcome):
    from_date = datetime.strptime(from_date_str, "%b %d %Y")
    outcome_date = datetime.strptime(outcome, "%b %d %Y")
    assert outcome_date == rule_price_earning_ratio.extract_date(date_range, from_date)


@pytest.fixture
def load_stock_a():
    stock_a = os.path.join(os.getcwd(), "rules/tests/", "test_data_stock_a.csv")
    df_stock_a = pd.read_csv(stock_a)
    df_stock_a['date'] = pd.to_datetime(df_stock_a['date']).dt.date
    return df_stock_a


@pytest.mark.parametrize("percentile_threshold, date_range, outcome", [
    ("0.1", "1m", False),
    ("0.2", "1m", True),
    ("0.5", "1m", True),
])
def test_filter_by_percentile(load_stock_a, percentile_threshold, date_range, outcome):
    assert outcome == rule_price_earning_ratio.filter_by_percentile(load_stock_a, percentile_threshold, date_range)
