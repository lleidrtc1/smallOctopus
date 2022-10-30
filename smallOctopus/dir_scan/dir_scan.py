# coding=utf-8
"""
目录扫描程序
"""
import sys
# 设置环境变量
sys.path.append("../")
import math
import os
from queue import Queue
import threading
import requests
from fake_useragent import UserAgent

from smallOctopus.config import d_thread_count, d_url


class Dir_scan(object):
    def __init__(self, url, thread_count):
        self._thread_count = thread_count
        self._url = url
        self._queue = Queue()
        self._result = []
        self._threads = []
        self._total_count = 0

    def _init(self):
        """
        初始化：url+字典拼接保存到queue
        :return:
        """
        with open("./dir_scan/dict/php.txt", 'r') as f:
            for d in f:
                if "://" in self._url:
                    self._queue.put(self._url.rstrip().rstrip("/") + "/" + d.strip("/"))
                else:
                    self._queue.put("http://" + self._url.rstrip().rstrip("/") + "/" + d.rstrip("/"))
                    self._queue.put("https://" + self._url.rstrip().rstrip("/") + "/" + d.strip("/"))
        self._total_count = self._queue.qsize()

    def start(self):
        self._init()
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Dir_scan_run(self._queue, self._result, self._total_count))
        # 开启
        for t in self._threads:
            t.start()
        # 结束
        for t in self._threads:
            t.join()
        # 汇集结果
        if "://" in self._url:
            temp = self._url.rstrip("/").split("://")
            base_path = temp[1].split("/")[0]
        else:
            base_path = self._url.rstrip("/")
        if os.path.exists(f"./dir_scan/dict/{base_path}_dirs.txt"):
            os.remove(f"./dir_scan/dict/{base_path}_dirs.txt")
        with open(f"./dir_scan/dict/{base_path}_dirs.txt", 'a+') as f:
            for r in self._result:
                f.write(r + "\n")

    class Dir_scan_run(threading.Thread):
        def __init__(self, queue, result, total_count):
            super().__init__()
            self._total_count = total_count
            self._result = result
            self._queue = queue

        def run(self):
            headers = {
                "User-Agent": UserAgent().random
            }
            while not self._queue.empty():
                scan_url = self._queue.get().rstrip()
                last = self._queue.qsize()
                self.msg(last)
                try:
                    res = requests.get(scan_url, headers=headers)
                    if res.status_code == 200:
                        self._result.append(scan_url)

                except Exception as e:
                    pass

        def msg(self, last):
            """
            进度条
            :return:
            """
            last = round((last / self._total_count), 3)
            already_do = round((1 - last) * 100, 3)
            sys.stdout.write(f"\r[*][{math.floor(already_do) * '='}>{math.floor(last * 100) * '.'}]已完成{already_do}%")


t = Dir_scan(d_url, d_thread_count)
t.start()
