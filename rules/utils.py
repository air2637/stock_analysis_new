import os
import datetime


def save_result(stock_wanted, result_loc, rule_name):
    """
    A utility function saves resulted stocks at the specified location, with rule's name as well as a timestamp

    :param stock_wanted: a dataframe consists of stocks
    :param result_loc: a relative path for saving the resulted stocks in csv
    :param rule_name: the name of the rule, based on which the result is derived from
    :return: the absolute path of the saved result
    """
    file_name = "".join((rule_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), ".csv"))
    saved_path = os.path.join(os.getcwd(), result_loc, file_name)
    stock_wanted.to_csv(saved_path)
    return saved_path
