from meizhuangshibie import main as meizhuangrun
from baidushibie import run as baidurun
from hebing import run as hebingrun
import pymysql
from sqlalchemy import create_engine


def run():
    meizhuangrun()
    baidurun()
    hebingrun()


if __name__ == '__main__':
    run()