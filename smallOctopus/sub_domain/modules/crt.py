# coding=utf-8
"""
从https://crt.sh收集子域名
"""
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def is_domain(domain):
    """
    判断是否是有效域名
    :param domain:
    :return:
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9])).'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if pattern.match(domain) else False


class Crt_spider(object):
    def __init__(self, domain):
        self._source_url = "https://crt.sh/?q="
        self._domain = domain

    def start(self):
        print("crt开始扫描......")
        scan_url = self._source_url + self._domain
        headers = {
            "UserAgent": UserAgent().random,
            "Referer": "https://crt.sh"
        }
        # 发起请求
        flag = True
        max_count = 0
        response = ''
        while flag and max_count <= 16:
            try:
                response = requests.get(scan_url, headers=headers, timeout=2)
                max_count += 1
                if response.status_code == 200:
                    flag = False
            except Exception as e:
                pass

        # 开始提取内容
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        # 解析子域名
        tds = soup.find_all(name="td", attrs={"style": None, "class": None})
        domain_list = []
        for td in tds:
            try:
                if is_domain(td.string):
                    domain_list.append(td.string)
            except Exception as e:
                pass
        # 去重
        domain_list = list(set(domain_list))
        # save
        save_path = f"./sub_domain/cache/crt/{self._domain}.txt"
        if os.path.exists(save_path):
            os.remove(save_path)
        with open(save_path, "a+") as f:
            json.dump(domain_list, f, indent=4)
        print("crt扫描结束，已保存！！！！！！")

# domain = "wuyecao.net"
# t = Crt_spider(domain)
# t.start()
