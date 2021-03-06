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
    result_files = []
    for each_rule_config in config_stock_filter_rules["rules"]:
        rule_name = ""
        rule_params = {}
        for rule_config, rule_config_val in each_rule_config.items():
            logger.info('rule_config -- %s: %s', rule_config, rule_config_val)
            if rule_config != "enabled":
                rule_name = rule_config
                rule_params = rule_config_val
            elif rule_config == "enabled" and rule_config_val:
                result_file = stock_filter_rule.call_rule(rule_name, rule_params)
                result_files.append(result_file)
    # combine results from result files and apply logic gate
    stock_filter_rule.combine_rule_results(result_files, config_stock_filter_rules["logic_gates"])


if __name__ == '__main__':
    download_raw_data()
    filter_stock_with_rules()

