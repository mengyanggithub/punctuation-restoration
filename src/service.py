# -*- coding: utf-8 -*-
# @Time    : 2021/7/2 09:50
# @Author  : buer
# @FileName: server.py
# @Software: IntelliJ IDEA
import os
import json
import time
from sanic import Sanic
from sanic.request import Request
from sanic.response import text, json as reponse
from sanic.log import logger, error_logger
import traceback

if not os.path.exists("logs"):
    os.makedirs("logs")

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "ERROR",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            "formatter": "generic",
            'filename': 'logs/app.log',
            'when': 'D',
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        "error_console": {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'generic',
            'filename': 'logs/error.log',
            'when': 'D',
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        "access_console": {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'access',
            'filename': 'logs/access.log',
            'when': 'D',
            'backupCount': 3,
            'encoding': 'utf-8'
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
                      + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)
app = Sanic("func_restore", log_config=LOGGING_CONFIG)


def get_json(request: Request):
    post_data = request.json
    if not post_data:
        post_data = request.form
    if not post_data:
        post_data = request.args
    if not post_data:
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
    return post_data


def process_request(request, parameters, func, optional_parameters=None):
    st = time.time()
    try:
        post_data = get_json(request)
        info = 'post data: %s' % post_data
        logger.info(info[:500])
        for param in parameters:
            if param not in post_data:
                result = {'msg': "missing parameter %s" % param, 'code': -1}
                error_logger.error("missing parameter %s" % param)
                return reponse(result, ensure_ascii=False)

        kwargs = {}
        if optional_parameters is not None:
            for param in optional_parameters:
                if param in post_data:
                    kwargs[param] = post_data[param]

        result = func(*[post_data[param] for param in parameters], **kwargs)
        info = "result: %s" % result
        logger.info(info[:500])
        result = {"result": result, 'msg': "success", 'code': 200, 'cost_time': time.time() - st}
        return reponse(result, ensure_ascii=False)
    except Exception as e:
        result = {'msg': str(e), 'code': -1, 'cost_time': time.time() - st}
        error_logger.error(traceback.format_exc())
        return reponse(result, ensure_ascii=False)


def log_info(info):
    logger.info(info)


def return_text(content):
    return text(content)
