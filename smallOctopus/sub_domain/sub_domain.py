# coding=utf-8
import json
import sys
# 设置环境变量
sys.path.append("../")

from smallOctopus.config import domain
from smallOctopus.sub_domain.modules.brute import Brute
from smallOctopus.sub_domain.modules.crt import Crt_spider

t = Crt_spider(domain)
t.start()
t = Brute(domain, 10)
t.start()


def out_put(domain):
    """
    最后的输出方法
    :param domain: 域名
    :return:
    """
    # 准备一个大的列表
    domain_unique = []
    crt_save_path = f"./sub_domain/cache/crt/{domain}.txt"
    brute_save_path = f"./sub_domain/cache/brute/{domain}.txt"

    with open(crt_save_path, "r") as f:
        data = json.load(f)
        domain_unique += data
    with open(brute_save_path, "r") as f:
        data = json.load(f)
        domain_unique += data
    # 去重
    domain_unique = list(set(domain_unique))
    # 输出
    print("~~~~~~~~~~~~~~~~~最终结果~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for d in domain_unique:
        print(d)


out_put(domain)
