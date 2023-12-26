#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created By  : chenrong
# Created Date: 2023/12/15
# Filename    : stocks.py


from os import path
from typing import Optional
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from api import StockUtil
from config.conf import stock_file

templates_path = path.dirname(path.dirname(__file__))
templates = Jinja2Templates(directory=f"{templates_path}/templates")
router = APIRouter()


class Item(BaseModel):
    code: str


@router.get("/")
def index(request: Request):
    _data = StockUtil.query_stocks_data(file=stock_file)
    stocks_list = StockUtil.read_stocks_file(file=stock_file)
    # 按照配置文件排序
    data = StockUtil.sort_list(data=_data, list=stocks_list)
    return templates.TemplateResponse("price.html", {"request": request, "data": data})


# 查询价格
@router.api_route("/stocks/price", methods=["GET", "POST"])
def list(request: Request):
    if request.method == 'GET':
        res = RedirectResponse(url="/", status_code=302)
        return res
    if request.method == 'POST':
        _data = StockUtil.query_stocks_data(file=stock_file)
        stocks_list = StockUtil.read_stocks_file(file=stock_file)
        # 按照配置文件排序
        data = StockUtil.sort_list(data=_data, list=stocks_list)
        return data


# 添加自选
@router.api_route("/stocks/add", methods=["GET", "POST"])
def add(request: Request,
        code: str = Form(None),
        ):
    if request.method == 'GET':
        res = RedirectResponse(url="/", status_code=302)
        return res
    if request.method == 'POST':
        rs = StockUtil.add_stock(code=code, file=stock_file)
        return {"action": "add", "code": code, "result": rs}


# 删除自选
@router.api_route("/stocks/delete", methods=["GET", "POST"])
def delete(request: Request,
           item: Optional[Item] = None
           ):
    if request.method == 'GET':
        res = RedirectResponse(url="/", status_code=302)
        return res
    if request.method == 'POST':
        code = item.code
        rs = StockUtil.remove_stock(code=code, file=stock_file)
        return {"action": "delete", "code": code, "result": rs}


# 置顶自选
@router.api_route("/stocks/change", methods=["GET", "POST"])
def change(request: Request,
           item: Optional[Item] = None
           ):
    if request.method == 'GET':
        res = RedirectResponse(url="/", status_code=302)
        return res
    if request.method == 'POST':
        code = item.code
        rs = StockUtil.totop_stock(code=code, file=stock_file)
        return {"action": "totop", "code": code, "result": rs}
