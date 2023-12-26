#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from os import path
from routers import stocks

app = FastAPI()

origins = [
    "http://172.16.21.227:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = path.dirname(__file__)

app.mount("/static", StaticFiles(directory=f"{static_path}/static"), name="static")
app.include_router(stocks.router)

if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app='main:app',
                host="0.0.0.0",
                port=8000,
                reload=True,
                proxy_headers=True,
                forwarded_allow_ips="10.0.1.5",
                log_config=log_config)
