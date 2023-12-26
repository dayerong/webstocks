#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created By  : chenrong
# Created Date: 2023/12/15
# Filename    : StockUtil.py

import os
import akshare as ak

"""
安装：pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade

"""


def read_stocks_file(file):
    if not os.path.isfile(file):
        f = open(file, 'w')
        f.close()

    try:
        with open(file, 'r') as f:
            _stocks = [line.strip('\n') for line in f.readlines()]
            return _stocks
    except Exception as e:
        print(e)
        return False


def check_stock(code):
    try:
        ak.stock_individual_info_em(symbol=code)
        return True
    except:
        return False


def query_stocks_data(file):
    self_stocks = read_stocks_file(file)
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    stocks = stock_zh_a_spot_em_df[stock_zh_a_spot_em_df['代码'].isin([str(i) for i in self_stocks])].iloc[:,
             [1, 2, 3, 4, 5]]
    _data_list = []

    def check_nan(element):
        import math

        n = float(element)
        rs = math.isnan(n)
        return rs

    for _, row in stocks.iterrows():
        _data_dict = {}
        _data_dict["代码"] = row['代码']
        _data_dict["名称"] = row['名称']
        _data_dict["最新价"] = ["--" if check_nan(row['最新价']) else row['最新价']][0]
        _data_dict["涨跌幅"] = ["--" if check_nan(row['涨跌幅']) else row['涨跌幅']][0]
        _data_list.append(_data_dict)
    return _data_list


def check_vaild(code, file):
    """
    返回码     描述
    1000       股票代码不存在
    1001       股票已在自选中
    1002       股票不在自选中
    """
    if not check_stock(code):
        return 1000

    _stock = read_stocks_file(file)
    if code in _stock:
        return 1001
    else:
        return 1002


def remove_stock(code, file):
    with open(file, "r") as infile:
        lines = infile.readlines()

    try:
        with open(file, "w") as outfile:
            for line in lines:
                if line.strip('\n') != code:
                    outfile.write(line)
        return True
    except Exception as e:
        print(e)
        return False


def add_stock(code, file):
    """
    返回码     描述
    1003       添加成功
    """
    rs = check_vaild(code, file)
    if rs == 1000 or rs == 1001:
        return rs

    if rs == 1002:
        with open(file, mode='a') as f:
            f.write(code + '\n')
        return 1003


def totop_stock(code, file):
    with open(file, "r") as infile:
        lines = infile.readlines()
        original_list = [i.strip('\n') for i in lines]

    original_list.remove(code)
    original_list.insert(0, code)

    try:
        with open(file, "w") as outfile:
            for i in original_list:
                outfile.write(i + '\n')
        return True
    except Exception as e:
        print(e)
        return False


def sort_list(data, list):
    _data = []
    for i in list:
        for l in data:
            if l.get("代码") == i:
                _data.append(l)
    return _data


def check_nan(element):
    import math

    n = float(element)
    rs = math.isnan(n)
    return rs
