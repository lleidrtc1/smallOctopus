# coding=utf-8
"""
字典暴力破解子域名
"""
import json
import math
import os
import sys
from queue import Queue
import requests
import threading
from fake_useragent import UserAgent


class Brute(object):
    def __init__(self, domain, thread_count):
        self._domain = domain
        self._queue = Queue()
        self._thread_count = thread_count
        self._threads = []
        self._total_count = 0
        self._result = []

    def _init(self):
        """
        初始化，生成拼接的域名
        :return:
        """
        # 读取字典的内容
        with open("./sub_domain/dict/domain.txt", "r") as f:
            for d in f:
                # 拼接域名
                scan_domain = d.strip() + "." + self._domain
                # 将域名放入队列
                self._queue.put("http://" + scan_domain)
        self._total_count = self._queue.qsize()

    def start(self):
        print("brute模块开始执行......")
        # 初始化
        self._init()
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Brute_run(self._queue, self._total_count, self._result))
        # 启动
        for t in self._threads:
            t.start()
        # 等待子线程结束
        for t in self._threads:
            t.join()

        # 保存结果
        save_path = f"./sub_domain/cache/brute/{self._domain}.txt"
        if os.path.exists(save_path):
            os.remove(save_path)
        with open(save_path, "a+") as f:
            json.dump(self._result, f, indent=4)
        print("\nbrute模块运行完成！")

    class Brute_run(threading.Thread):
        def __init__(self, queue, total_count, result):
            super().__init__()
            self._queue = queue
            self._total_count = total_count
            self._result = result

        def run(self):
            headers = {
                "UserAgent": UserAgent().random
            }
            while not self._queue.empty():
                scan_domain = self._queue.get()
                self._msg()
                # 显示进度
                try:
                    response = requests.get(scan_domain, headers=headers, timeout=2)
                    if response.status_code != 404:
                        # 存放在一个result
                        self._result.append(scan_domain.lstrip("http://"))
                except Exception as e:
                    pass

        def _msg(self):
            last = round((self._queue.qsize() / self._total_count) * 100, 3)
            already_do = round(100 - last, 3)
            sys.stdout.write(f"\r[{math.floor(already_do) * '='}>{math.floor(last) * '.'}]已扫描{already_do}%")


# domain = "wuyecao.net"
# t = Brute(domain, 10)
# t.start()
