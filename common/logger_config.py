#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import logging,os
LOG_FILE = 'wetest.log'


def makesure_dir_exist(path):
    existed=os.path.exists(path)
    if existed:
        return True
    else:
        os.mkdir(path)

handler = logging.StreamHandler()
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger()    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler

#mode=os.environ.get("RUNNER_MODE")

log_dir=os.environ.get("UPLOADDIR")
file_path = os.path.split(os.path.realpath(__file__))[0]
if log_dir:
    file_path=os.path.abspath(os.path.join(log_dir,"python_log.log"))
else:
    log_name="../../python_log_{0}.log".format(os.environ.get("ADB_SERIAL",""))
    file_path=os.path.abspath(os.path.join(file_path,log_name))
file_handler=logging.FileHandler(file_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


logger.setLevel(logging.DEBUG)


def get_logger():
    if not get_logger.instance:
        get_logger.instance=logging.getLogger("wetest")
    return get_logger.instance


get_logger.instance=None