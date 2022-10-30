# coding=utf-8
"""
爬取http://www.66ip.cn/的免费代理ip
"""
import math
import os
import re
import sys
# 设置环境变量
sys.path.append("../")
import threading
import requests
from bs4 import BeautifulSoup
from queue import Queue
from fake_useragent import UserAgent

from smallOctopus.config import ip_thread_count


class Proxy_ip_spider(object):
    def __init__(self, thread_count):
        self._thread_count = thread_count
        self._base_url = "http://www.66ip.cn/"
        self._queue = Queue()
        self._total_count = 0
        self._result = []
        self._threads = []

    def _init_url(self):
        """
        获取目标网站的url列表
        :return:
        """
        base_path = self._base_url.rstrip("/").split("://")
        if os.path.exists(f"./proxy_ip_spider/cache/{base_path[1]}_urls.log"):
            os.remove(f"./proxy_ip_spider/cache/{base_path[1]}_urls.log")
        response = requests.get(self._base_url)
        html = response.content.decode("gb2312")
        soup = BeautifulSoup(html, 'lxml')
        all_url = soup.find_all(name="a", attrs={"href": re.compile("^/areaindex_")})
        # 把目标url保存在cache中
        with open(f"./proxy_ip_spider/cache/{base_path[1]}_urls.log", "a+") as f:
            for a in all_url:
                f.write(self._base_url.rstrip("/") + a['href'] + "\n")

    def _init_queue(self):
        """
        初始化需要爬取的队列
        :return:
        """
        base_path = self._base_url.rstrip("/").split("://")
        with open(f"./proxy_ip_spider/cache/{base_path[1]}_urls.log", "r") as f:
            for u in f:
                self._queue.put(u.rstrip())
        self._total_count = self._queue.qsize()

    def start(self):
        self._init_url()
        self._init_queue()
        print("正在扫描......")
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Thread_run(self._queue, self._result, self._total_count))
        for t in self._threads:
            t.start()
        for t in self._threads:
            t.join()
        # 写入文件

        base_path = self._base_url.rstrip("/").split("://")
        if os.path.exists(f"./proxy_ip_spider/cache/{base_path[1]}_proxy_ip.txt"):
            os.remove(f"./proxy_ip_spider/cache/{base_path[1]}_proxy_ip.txt")
        with open(f"./proxy_ip_spider/cache/{base_path[1]}_proxy_ip.txt", "a+") as f:
            for r in self._result:
                f.write(r + "\n")

        print("代理ip写入成功!!!!!!")

    class Thread_run(threading.Thread):
        """
        专门跑线程的内部类
        """

        def __init__(self, queue, result, total_count):
            super().__init__()
            self._total_count = total_count
            self._result = result
            self._queue = queue

        def msg(self):
            """
            显示进度
            :return:
            """
            last = round((self._queue.qsize() / self._total_count) * 100, 3)
            already_do = round(100 - last, 3)
            sys.stdout.write(f"\r[{math.floor(already_do) * '='}>{math.floor(last) * '.'}]已扫描{already_do}%")
            if already_do==100:
                print("\n等待中......")
        def run(self):
            headers = {
                "User-Agent": UserAgent().random
            }
            while not self._queue.empty():
                response = requests.get(self._queue.get(), headers=headers, timeout=2)
                self.msg()
                html = response.content.decode("gb2312")
                soup = BeautifulSoup(html, 'lxml')
                # 先找表
                table = soup.find("table", bordercolor="#6699ff")
                # 再找其中的tr>td
                trs = table.find_all("tr")
                # 删掉第一个tr
                del (trs[0])
                for tr in trs:
                    tds = tr.find_all("td")
                    ip = tds[0].string
                    port = tds[1].string
                    ip_port = ip + ":" + port
                    # 验证代理ip是否可用
                    url_test_proxy = "http://httpbin.org/ip"
                    proxy = {
                        "http": f"http://{ip_port}",
                        "https": f"https://{ip_port}"
                    }
                    try:
                        res = requests.get(url_test_proxy, proxies=proxy, timeout=2)
                        # 判断结果
                        res_html = res.text
                        if ip in res_html:
                            self._result.append(ip_port)

                    except Exception as e:
                        pass


ip = Proxy_ip_spider(ip_thread_count)
ip.start()
