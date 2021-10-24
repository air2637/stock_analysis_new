import os
import datetime


def save_result(stock_wanted, result_loc, rule_name):
    file_name = "".join((rule_name, datetime.datetime.now().strftime("%d%m%Y_%H%M%S"), ".csv"))
    saved_path = os.path.join(os.getcwd(), result_loc, file_name)
    stock_wanted.to_csv(saved_path)
    return saved_path
