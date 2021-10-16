import importlib
from analysis_config import *
from rules import stock_filter_rule
from data_crawler import data_crawler
from setup_logging import logger


def download_raw_data():
    """ Ideally it can download corresponding data based on param passes in
        :param data_name
        :param stored_loc
        :param source_loc
        shall I create a config(dictionary) like below?
        download_raw_data = {
            data_name: xxx
            stored_loc: xxx
            source_loc: xxx
            refresh_flag: True/False
        }
    """
    for data_store in config_download_raw_data["data_stores"]:
        # breakpoint()
        logger.info("To refresh data store %s? -> %s", data_store["store_name"], data_store["refresh_now"])
        if data_store["refresh_now"]:
            data_crawler.crawl_by(data_store["extract_func"], data_store)




def filter_stock_with_rules():
    """ Ideally it should take in a tuple of rules with logic gates
        :param rules tuple -> filter_rule[]?
        filter_rule = {
            rule_name: xxx
            rule_func: some_func()
            filtered_result: [{stock_id: xxx, result: some_value}, {}, {}]
        }
        logic gates to apply to the filtered_result of the rules
    """
    for each_rule_config in config_stock_filter_rules["rules"]:
        for rule_name, rule_params in each_rule_config.items():
            logger.info('rule_name: %s', rule_name)
            for key in rule_params:
                logger.info('param: %s = %s', key, rule_params[key])

            stock_filter_rule.call_rule(rule_name, rule_params)


if __name__ == '__main__':
    download_raw_data()
    filter_stock_with_rules()

